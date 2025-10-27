## **app/main.py**
Đây là điểm khởi đầu (entry point) của ứng dụng. Nó chứa instance của FastAPI (app = FastAPI()) và nơi bạn bao gồm (include) các APIRouter từ thư mục api/.

## **app/api/**
Thư mục này chứa tất cả các định nghĩa API Endpoints (đường dẫn).

- **endpoints/**: Chứa các file định nghĩa APIRouter cho từng module/resource (ví dụ: user.py, item.py). Mỗi file này sẽ định nghĩa các hàm xử lý cho các request GET, POST, PUT, DELETE.

## **app/schemas/**
Chứa các Pydantic models. Pydantic được FastAPI sử dụng để:
- Xác thực dữ liệu (Data Validation) đầu vào từ request body, query parameters.
- Định nghĩa cấu trúc dữ liệu trả về từ API (Response Models).
- Đảm bảo kiểu dữ liệu an toàn (type safety).

## **app/models/**
Chứa các Mô hình cơ sở dữ liệu (Database Models), ví dụ các model SQLAlchemy hoặc SQLModel. Chúng định nghĩa cấu trúc của các bảng trong cơ sở dữ liệu.

## **app/services/**
Chứa Logic nghiệp vụ (Business Logic) phức tạp, nơi thực hiện các quy tắc, tính toán của ứng dụng. Nó sử dụng các hàm từ app/crud/ để tương tác với DB và xử lý dữ liệu trước khi trả về cho endpoint.

## **app/core/**
Chứa các module cốt lõi, không liên quan đến một module nghiệp vụ cụ thể nào.
- **config.py:** Xử lý việc tải các biến môi trường (Environment Variables) hoặc các cài đặt ứng dụng.
- **security.py:** Chứa các hàm xử lý bảo mật như hashing mật khẩu, mã hóa/giải mã JWT.

## **app/dependencies.py**
Nơi định nghĩa các hàm Dependency Injection của FastAPI. Ví dụ phổ biến là hàm get_db để cung cấp một session cơ sở dữ liệu cho các endpoint hoặc service.