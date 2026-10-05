import * as ftp from "basic-ftp";
import dotenv from "dotenv";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.join(__dirname, ".env") });

const {
  FTP_HOST,
  FTP_USER,
  FTP_PASSWORD,
  FTP_PORT = "21",
  FTP_REMOTE_ROOT = "public_html",
  FTP_SECURE = "false",
} = process.env;

if (!FTP_HOST || !FTP_USER || !FTP_PASSWORD) {
  console.error("\n❌ Помилка: Не заповнено дані для FTP у файлі .env!");
  console.error("Будь ласка, перевірте файл .env у корені проєкту. Потрібні змінні:");
  console.error("  FTP_HOST=uashared40.twinservers.net (або IP)");
  console.error("  FTP_USER=ваш_логін");
  console.error("  FTP_PASSWORD=ваш_пароль");
  console.error("  FTP_REMOTE_ROOT=public_html");
  console.error("  FTP_SECURE=false (або explicit)\n");
  process.exit(1);
}

async function deploy() {
  const client = new ftp.Client();
  client.ftp.verbose = true;

  try {
    console.log(`\n🚀 Підключення до FTP-сервера ${FTP_HOST}:${FTP_PORT}...`);
    await client.access({
      host: FTP_HOST,
      user: FTP_USER,
      password: FTP_PASSWORD,
      port: parseInt(FTP_PORT, 10),
      secure: FTP_SECURE === "true" || FTP_SECURE === "explicit",
      secureOptions: {
        rejectUnauthorized: false,
      },
    });

    console.log("✅ Успішно підключено!");
    const localDistPath = path.join(__dirname, "dist");
    console.log(`📁 Завантаження файлів з dist/ у віддалену папку '${FTP_REMOTE_ROOT}'...`);

    await client.ensureDir(FTP_REMOTE_ROOT);
    await client.uploadFromDir(localDistPath);

    console.log("\n🎉 ДЕПЛОЙ УСПІШНО ЗАВЕРШЕНО!");
    console.log(`Файли сайту оновлено на сервері у папці '${FTP_REMOTE_ROOT}'.\n`);
  } catch (err) {
    console.error("\n❌ Помилка під час деплою:", err.message);
    process.exit(1);
  } finally {
    client.close();
  }
}

deploy();
