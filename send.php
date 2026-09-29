<?php
/**
 * АлмазПрофиБур — отправка заявок с сайта в CRM Битрикс24.
 *
 * НАСТРОЙКА (один раз):
 * 1. Битрикс24 → Разработчикам → Другое → Входящий вебхук.
 * 2. Права: только «CRM (crm)». Сохраните.
 * 3. Скопируйте адрес вебхука (вида https://ваш-портал.bitrix24.ru/rest/1/abc123xyz/)
 *    и вставьте его в B24_WEBHOOK ниже.
 *
 * Адрес вебхука — это ключ доступа к вашей CRM. Не вставляйте его в HTML/JS
 * и никому не пересылайте. Этот файл выполняется на сервере, посетители его код не видят.
 */

const B24_WEBHOOK = ''; // ← например: 'https://almazprofibur.bitrix24.ru/rest/1/abc123xyz/'
const ASSIGNED_BY_ID = 0; // ID ответственного сотрудника в Битрикс24 (0 = по умолчанию)

// -------------------------------------------------------------------------

header('Content-Type: application/json; charset=utf-8');

function reply(int $code, array $data): void {
    http_response_code($code);
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    reply(405, ['ok' => false, 'error' => 'method_not_allowed']);
}

if (B24_WEBHOOK === '') {
    reply(500, ['ok' => false, 'error' => 'webhook_not_configured']);
}

$in = json_decode(file_get_contents('php://input'), true);
if (!is_array($in)) {
    reply(400, ['ok' => false, 'error' => 'bad_request']);
}

// Спам-бот заполнил скрытое поле — делаем вид, что всё хорошо, но в CRM ничего не пишем
if (!empty($in['website'])) {
    reply(200, ['ok' => true]);
}

function clean($v, int $max = 300): string {
    $v = trim(strip_tags((string)($v ?? '')));
    return mb_substr($v, 0, $max);
}

$type   = ($in['type'] ?? '') === 'messenger' ? 'messenger' : 'callback';
$name   = clean($in['name'] ?? '', 100);
$phone  = clean($in['phone'] ?? '', 30);
$source = clean($in['source'] ?? 'Заявка с сайта', 150);
$digits = preg_replace('/\D/', '', $phone);

if ($type === 'callback') {
    if (strlen($digits) !== 11) {
        reply(422, ['ok' => false, 'error' => 'bad_phone']);
    }
    // Без согласия на обработку ПДн заявку не принимаем (152-ФЗ)
    if (empty($in['consent'])) {
        reply(422, ['ok' => false, 'error' => 'no_consent']);
    }
}

// Простая защита от повторных отправок: не чаще 1 заявки в 20 секунд с одного IP
$ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$lock = sys_get_temp_dir() . '/apb_lead_' . $type . '_' . md5($ip);
if (file_exists($lock) && time() - filemtime($lock) < 20) {
    reply(429, ['ok' => false, 'error' => 'too_many_requests']);
}
@touch($lock);

$total = (int)($in['total'] ?? 0);

$comments = implode("<br>", array_filter([
    'Форма: ' . $source,
    'Расчёт калькулятора: ' . clean($in['params'] ?? ''),
    'Материал: ' . clean($in['material'] ?? '', 50),
    'Диаметр: ' . (int)($in['diameter'] ?? 0) . ' мм',
    'Толщина стены: ' . (int)($in['depth'] ?? 0) . ' см',
    'Отверстий: ' . (int)($in['holes'] ?? 0) . ' шт.',
    'Страница: ' . clean($in['page'] ?? '', 500),
    $type === 'callback'
        ? 'Согласие на обработку ПДн: получено ' . date('d.m.Y H:i') . ' (IP ' . $ip . ')'
        : 'Клиент перешёл в мессенджер — контактов нет, ждите его сообщения',
]));

$fields = [
    'TITLE'              => ($type === 'messenger' ? 'Мессенджер: ' : 'Сайт: ') . $source,
    'NAME'               => $name !== '' ? $name : 'Без имени',
    'SOURCE_ID'          => 'WEB',
    'SOURCE_DESCRIPTION' => 'almazprofibur.ru — ' . $source,
    'COMMENTS'           => $comments,
    'OPPORTUNITY'        => $total,
    'CURRENCY_ID'        => 'RUB',
    'UTM_SOURCE'         => clean($in['utm_source'] ?? '', 100),
    'UTM_MEDIUM'         => clean($in['utm_medium'] ?? '', 100),
    'UTM_CAMPAIGN'       => clean($in['utm_campaign'] ?? '', 100),
    'UTM_CONTENT'        => clean($in['utm_content'] ?? '', 100),
    'UTM_TERM'           => clean($in['utm_term'] ?? '', 100),
];
if ($type === 'callback') {
    $fields['PHONE'] = [['VALUE' => $phone, 'VALUE_TYPE' => 'WORK']];
}
if (ASSIGNED_BY_ID > 0) {
    $fields['ASSIGNED_BY_ID'] = ASSIGNED_BY_ID;
}

$ch = curl_init(rtrim(B24_WEBHOOK, '/') . '/crm.lead.add.json');
curl_setopt_array($ch, [
    CURLOPT_POST           => true,
    CURLOPT_POSTFIELDS     => http_build_query([
        'fields' => $fields,
        'params' => ['REGISTER_SONET_EVENT' => 'Y'], // уведомление ответственному
    ]),
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT        => 15,
]);
$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlErr  = curl_error($ch);
curl_close($ch);

$result = json_decode((string)$response, true);

if ($curlErr || $httpCode !== 200 || empty($result['result'])) {
    error_log('[B24 lead] HTTP ' . $httpCode . ' ' . $curlErr . ' ' . $response);
    reply(502, ['ok' => false, 'error' => 'crm_error']);
}

reply(200, ['ok' => true, 'lead_id' => $result['result']]);
