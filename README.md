# Pest Detection FastAPI Backend

Backend REST API untuk deteksi hama (belalang dan ulat) menggunakan FastAPI dan model YOLO. API ini menyediakan endpoint untuk upload gambar, deteksi hama, dan riwayat deteksi dengan pagination.

## Prasyarat

- **Python 3.11+**: Pastikan Python sudah terinstall (`python --version`).
- **PostgreSQL**: Database untuk menyimpan data (opsional, bisa ganti SQLite).
- **Git**: Untuk clone repository ini.

## Struktur Proyek

```
└── 📁alembic
        └── env.cpython-311.pyc
    └── 📁versions
            └── 8c7212f007b8_create_uploads_table.cpython-311.pyc
        └── 8c7212f007b8_create_uploads_table.py
    └── env.py
    └── README
    └── script.py.mako
└── 📁src
    └── 📁app
        └── __init__.py
            └── __init__.cpython-311.pyc
        └── cli.py
        └── 📁config
                └── database.cpython-311.pyc
            └── database.py
            └── test_db.py
        └── 📁controllers
            └── 📁api
                    └── AuthController.cpython-311.pyc
                    └── DetectionController.cpython-311.pyc
                └── AuthController.py
                └── DetectionController.py
        └── 📁models
                └── AuthModel.cpython-311.pyc
                └── UploadModel.cpython-311.pyc
            └── AuthModel.py
            └── UploadModel.py
        └── 📁routes
                └── v1.cpython-311.pyc
            └── v1.py
        └── 📁services
                └── DetectionService.cpython-311.pyc
                └── ServiceFactory.cpython-311.pyc
            └── DetectionService.py
            └── ServiceFactory.py
    └── 📁ml_models
        └── best.pt
└── .env
└── .gitignore
└── alembic.ini
└── LICENSE
└── README.md
└── requirements.txt
```

## Instalasi

### 1. Clone Repository

Clone proyek ini ke lokal:

```bash
git clone <repository-url>
cd dectionpest-fastapi-backend-restapi
```

### 2. Buat Virtual Environment

```bash
python -m venv .venv
```

#### MacOS/Linux

```bash
source .venv/bin/activate
```

#### Windows

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Buat file .env di root proyek untuk konfigurasi environment:

```bash
cp .env.example .env
```

Isi dengan contoh:

```bash
DATABASE_URL=postgresql://postgres@localhost:5432/pest
SECRET_KEY=d8Ywj4DCm8JoDocuPlcC8akDQuiIojLlVwGFYA40CUg=
```

- Ganti **DATABASE_URL** sesuai database kamu:
  - SQLite: DATABASE_URL=sqlite:///app.db
  - PostgreSQL: Sesuaikan username, password, dan nama database.
- **SECRET_KEY** bisa digenerate ulang kalau perlu (untuk keamanan).

Buat database pest:

#### Jika pakai PostgreSQL

```bash
psql -U postgres -c "CREATE DATABASE pest;"
```

#### Jika pakai MySQL

```bash
mysql -u root -p
```

```bash
CREATE DATABASE pest;
```

### 5. Inisialisasi Alembic

Alembic digunakan untuk migrasi database. Inisialisasi Alembic:

```bash
alembic init alembic
```

- Ini akan buat folder alembic/ dan file alembic.ini.

**Konfigurasi** alembic/env.py
Edit alembic/env.py supaya terhubung ke model dan .env:

```bash
from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

load_dotenv()
config = context.config
sqlalchemy_url = os.getenv("DATABASE_URL")
if sqlalchemy_url:
    config.set_main_option("sqlalchemy.url", sqlalchemy_url)
else:
    raise ValueError("DATABASE_URL not found in .env")

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from src.app.models.UploadModel import Upload
from src.app.config.database import Base
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 6. Buat Migrasi untuk Tabel uploads

Buat file migrasi pertama:

```bash
alembic revision -m "create uploads table"
```

Edit file di alembic/versions/xxxxxxx_create_uploads_table.py:

#### Jika pakai PostgreSQL

```bash
"""create uploads table

Revision ID: xxxxxxx
Revises:
Create Date: 2025-04-05 16:00:00

"""
from alembic import op
import sqlalchemy as sa

revision: str = 'xxxxxxx'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        "uploads",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("original_image", sa.String, nullable=False),
        sa.Column("detected_image", sa.String, nullable=False),
        sa.Column("detection_result", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now())
    )

def downgrade():
    op.drop_table("uploads")
```

#### Jika pakai MySQL

```bash
"""create uploads table

Revision ID: xxxxxxx
Revises:
Create Date: 2025-04-05 17:00:00

"""
from alembic import op
import sqlalchemy as sa

revision: str = 'xxxxxxx'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        "uploads",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("original_image", sa.String(255), nullable=False),
        sa.Column("detected_image", sa.String(255), nullable=False),
        sa.Column("detection_result", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now())
    )

def downgrade():
    op.drop_table("uploads")
```

### 7. Jalankan Migrasi

Jalankan migrasi untuk buat tabel uploads:

```bash
alembic upgrade head
```

Verifikasi
Cek tabel di PostgreSQL:

```bash
psql -U postgres -d pest -c "\dt"
```

### 8. Jalankan FastAPI
Jalankan aplikasi:

```bash
uvicorn src.app:app --reload
```

Buka browser di [http://localhost:8000/docs](http://localhost:8000/docs) untuk lihat Swagger UI.

### 9. Tes Swagger

Di Swagger UI (/docs):

- Upload Gambar:
  Endpoint: POST /api/v1/detect
  Klik "Try it out", upload file gambar, pilih model_version (v1 atau v2), lalu "Execute".
  Cek respons JSON dengan hasil deteksi.
- Lihat Riwayat:
  Endpoint: GET /api/v1/history
  Tambah parameter page=1 dan limit=10, lalu "Execute".
  Pastikan data muncul dengan pagination.
- Detail Deteksi:
  Endpoint: GET /api/v1/detect/{upload_id}
  Masukkan ID dari upload sebelumnya.
- Hapus Deteksi:
  Endpoint: DELETE /api/v1/detect/{upload_id}
  Masukkan ID untuk hapus data.

## Troubleshooting

"Connection refused": Pastikan PostgreSQL jalan dan DATABASE_URL benar.
"Module not found": Cek path src.app.models.UploadModel sesuai struktur proyek.
Model YOLO error: Pastikan file best.pt dan best_v2.pt ada di src/ml_models/.

## Catatan

Tabel users akan ditambah di V2 dengan migrasi baru (Coming Soon).
Simpan .env di .gitignore supaya aman.

## Collaborators

- [Muhammad Farhan Mustafa](https://github.com/farhanmustafa15)
- [Muhammad Daniel Krisna Halim Putra](https://github.com/bforbilly24)
