# MakeSense

Hack The Box · Linux · 5 November 2026

A WordPress site with a custom theme that encrypts form submissions in the
browser, using a key shipped in the JavaScript every visitor downloads. With
that key we could sign our own submissions, so the contact form became a way to
store code in the administrator's inbox. Taking the site over was the easy part;
root came from a password reused across the database, an SSH account and an
internal OCR service that saved files under any name we gave it.

**Chain**

1. AES-GCM key in `whisper-wrapper.js` → valid ciphertext for
   `save_voice_results`
2. stored XSS in the transcription shown to the admin bot → new administrator
3. plugin upload → command execution as `www-data`
4. `wp-config.php` password reused for SSH as `walter` and for Basic auth on
   `127.0.0.1:8001`
5. root OCR service writes `saved/<filename>` into a PHP-served directory →
   SUID bash → root

[Report (PDF)](makesense_pentest_report.pdf)
