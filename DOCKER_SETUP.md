# AgriERP Docker Setup

Hướng dẫn chạy dự án AgriERP với Docker.

## Yêu cầu

- Docker Desktop
- Docker Compose

## Cài đặt

### 1. Tạo file .env

```bash
cp .env.example .env
```

Chỉnh sửa file `.env` với thông tin database của bạn.

### 2. Build và chạy containers

```bash
# Build và start tất cả services
docker-compose up -d --build

# Hoặc chỉ chạy MySQL
docker-compose up -d mysql

# Chỉ chạy backend
docker-compose up -d backend
```

### 3. Kiểm tra logs

```bash
# Xem logs tất cả services
docker-compose logs -f

# Xem logs MySQL
docker-compose logs -f mysql

# Xem logs backend
docker-compose logs -f backend
```

### 4. Chạy migrations

```bash
docker-compose exec backend python manage.py migrate
```

### 5. Tạo superuser

```bash
docker-compose exec backend python manage.py createsuperuser
```

### 6. Collect static files

```bash
docker-compose exec backend python manage.py collectstatic --noinput
```

## Truy cập

- **Backend Django**: http://localhost:8008
- **MySQL**: localhost:3308
- **Redis**: localhost:6382

## Các lệnh hữu ích

```bash
# Dừng tất cả services
docker-compose down

# Dừng và xóa volumes (XÓA DỮ LIỆU!)
docker-compose down -v

# Restart một service
docker-compose restart backend

# Vào shell của backend
docker-compose exec backend bash

# Vào MySQL shell
docker-compose exec mysql mysql -u root -p

# Chạy Django shell
docker-compose exec backend python manage.py shell

# Chạy tests
docker-compose exec backend python manage.py test
```

## Cấu trúc Services

- **mysql**: MySQL 8.2 database
- **backend**: Django application
- **redis**: Redis cache (optional)

## Troubleshooting

### MySQL connection refused

Đợi MySQL khởi động hoàn toàn (khoảng 30 giây đầu tiên).

```bash
docker-compose logs mysql
```

### Backend không kết nối được database

Kiểm tra biến môi trường trong file `.env`:

```bash
docker-compose exec backend env | grep DB_
```

### Reset database

```bash
docker-compose down -v
docker-compose up -d mysql
# Đợi MySQL khởi động
docker-compose up -d backend
docker-compose exec backend python manage.py migrate
```

## Development

Để chạy development mode mà không dùng Docker:

1. Chỉ chạy MySQL:
   ```bash
   docker-compose up -d mysql redis
   ```

2. Chạy Django trên local:
   ```bash
   cd backend
   source venv/bin/activate
   python manage.py runserver 0.0.0.0:8008
   ```

## Production

Để deploy production, cần:

1. Tắt DEBUG mode trong `.env`
2. Đổi SECRET_KEY
3. Cấu hình ALLOWED_HOSTS
4. Sử dụng Gunicorn thay vì runserver
5. Thêm Nginx reverse proxy
