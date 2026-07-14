# 🤖 Discord Voice Idle Bots (Treo Bot Discord 24/7)

Dự án này giúp bạn tạo **2 con bot Discord** chạy song song cùng lúc, tự động kết nối vào các **Kênh thoại (Voice Channels)** được cấu hình sẵn và tự động kết nối lại nếu bị mất kết nối hoặc bị kick. Dự án đi kèm một web server tích hợp để bạn có thể chạy 24/7 hoàn toàn miễn phí trên các nền tảng đám mây như Render hoặc Koyeb.

---

## 📌 Hướng dẫn từng bước thiết lập Bot trên Discord

### Bước 1: Tạo Bot trên Discord Developer Portal
1. Truy cập trang web [Discord Developer Portal](https://discord.com/developers/applications).
2. Đăng nhập tài khoản Discord của bạn.
3. Nhấp vào nút **New Application** ở góc trên bên phải.
4. Đặt tên cho ứng dụng (ví dụ: `Treo Voice 1`) -> Nhấn **Create**.

### Bước 2: Đặt Tên & Cài đặt Ảnh đại diện (Avatar) cho Bot
1. Tại trang quản lý ứng dụng vừa tạo, chọn mục **General Information** ở danh sách bên trái.
2. Ở đây, bạn có thể:
   - Thay đổi tên hiển thị của bot tại mục **NAME**.
   - Tải ảnh lên làm ảnh đại diện tại mục **APP ICON**.
3. Nhấp vào nút **Save Changes** ở phía dưới để lưu lại.

### Bước 3: Lấy Token của Bot
1. Chọn mục **Bot** ở menu bên trái.
2. Tại đây, nhấp vào nút **Reset Token** và xác nhận.
3. Một chuỗi ký tự dài sẽ xuất hiện (ví dụ: `MTIzNDU2Nzg5MDEyMzQ1Njc4...`). Nhấp vào **Copy** và lưu nó lại vào một nơi an toàn. Đây là **Bot Token** dùng để cấu hình trong code.
4. **Bật Gateway Intents**: Cuộn xuống mục **Privileged Gateway Intents**, bật cả 3 tùy chọn sau lên:
   - **Presence Intent**
   - **Server Members Intent**
   - **Message Content Intent**
   - Nhấp **Save Changes** để lưu lại.

> [!NOTE]
> Lặp lại **Bước 1, 2, 3** cho con Bot thứ hai để lấy **Token thứ 2**.

### Bước 4: Lấy ID của Kênh thoại (Voice Channel ID)
Để lấy ID của phòng voice channel cần treo bot:
1. Mở Discord trên máy tính.
2. Vào **Cài đặt người dùng (User Settings)** -> **Nâng cao (Advanced)**.
3. Bật tùy chọn **Chế độ nhà phát triển (Developer Mode)**.
4. Quay lại danh sách kênh, nhấn chuột phải vào Kênh thoại bạn muốn bot nhảy vào -> Chọn **Sao chép ID Kênh (Copy Channel ID)**. Bạn sẽ nhận được một chuỗi số (ví dụ: `123456789012345678`).

### Bước 5: Mời (Invite) Bot vào Server của bạn
Để mời bot vào server của bạn:
1. Vào trang quản lý bot trên Developer Portal, chọn mục **OAuth2** -> **URL Generator** ở menu bên trái.
2. Tại mục **SCOPES**, tích chọn ô **bot**.
3. Tại mục **BOT PERMISSIONS** xuất hiện phía dưới, tích chọn các quyền sau:
   - **View Channel** (Xem kênh)
   - **Connect** (Kết nối kênh thoại)
   - **Speak** (Nói - cần thiết để bot tham gia vào phòng voice ổn định)
4. Cuộn xuống dưới cùng, sao chép đường dẫn tại mục **GENERATED URL**.
5. Dán liên kết đó vào trình duyệt của bạn, chọn server của bạn và nhấn **Ủy quyền (Authorize)** để mời bot vào server.

> [!NOTE]
> Làm tương tự cho cả 2 bot. Sau khi mời xong, hãy đảm bảo vai trò (role) của bot hoặc chính bot có đủ quyền tham gia và kết nối vào phòng voice channel mà bạn đã chọn.

---

## ⚙️ Cấu hình và Chạy thử nghiệm ở Local (Máy tính của bạn)

### 1. Cấu hình file `.env`
Mở file `.env` trong thư mục dự án và thay thế các thông tin bằng thông tin thật của bạn:
```env
# Bot 1 Configuration
BOT_TOKEN_1=Mã_Token_Bot_1_Của_Bạn
VOICE_CHANNEL_ID_1=ID_Kênh_Thoại_1_Của_Bạn

# Bot 2 Configuration
BOT_TOKEN_2=Mã_Token_Bot_2_Của_Bạn
VOICE_CHANNEL_ID_2=ID_Kênh_Thoại_2_Của_Bạn

# Port mặc định cho Web Server
PORT=8080
```

### 2. Cài đặt các thư viện cần thiết
Mở Terminal/PowerShell tại thư mục dự án và chạy lệnh sau để cài đặt các thư viện:
```bash
pip install -r requirements.txt
```

### 3. Chạy Bot
Chạy lệnh sau để khởi động cả 2 bot:
```bash
python main.py
```
Nếu thành công, bạn sẽ thấy log thông báo bot đã login và tự động nhảy vào các kênh thoại tương ứng.

---

## ☁️ Hướng dẫn treo Bot 24/7 Miễn phí trên Render.com

Để treo bot không cần mở máy, bạn có thể đưa mã nguồn này lên **Render.com** (hoàn toàn miễn phí):

### Bước 1: Đưa code lên GitHub
1. Tạo một repository mới trên tài khoản GitHub của bạn (ở chế độ **Private** hoặc **Public**).
2. Upload toàn bộ các file trong thư mục này lên GitHub (trừ file `.env` chứa token của bạn - vì bảo mật, không nên đẩy file `.env` lên GitHub).

### Bước 2: Tạo Web Service trên Render.com
1. Truy cập [Render.com](https://render.com/) và đăng ký/đăng nhập tài khoản bằng GitHub của bạn.
2. Trên Dashboard, nhấp vào **New +** -> Chọn **Web Service**.
3. Kết nối với Repository GitHub bạn vừa upload code lên ở Bước 1.
4. Cấu hình thông tin dịch vụ như sau:
   - **Name**: Đặt tên dự án (ví dụ: `my-discord-idle-bots`).
   - **Region**: Chọn khu vực gần bạn nhất (ví dụ: Singapore).
   - **Language**: `Python`
   - **Branch**: `main` (hoặc tên branch chứa code của bạn)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Instance Type**: Chọn gói **Free** (Miễn phí).

### Bước 3: Cấu hình Biến Môi trường (Environment Variables)
1. Trước khi deploy, cuộn xuống chọn tab **Advanced** (hoặc sau khi tạo, chọn mục **Environment** ở menu bên trái của Web Service).
2. Thêm các key-value tương tự như file `.env` local của bạn:
   - `BOT_TOKEN_1` = `<Token của Bot 1>`
   - `VOICE_CHANNEL_ID_1` = `<ID Kênh thoại 1>`
   - `BOT_TOKEN_2` = `<Token của Bot 2>`
   - `VOICE_CHANNEL_ID_2` = `<ID Kênh thoại 2>`
3. Nhấn **Save Changes** hoặc **Create Web Service**. 
4. Hệ thống sẽ bắt đầu xây dựng (build) và khởi chạy ứng dụng. Sau khi chạy xong, bạn sẽ thấy thông báo **Live** kèm theo một đường dẫn URL dạng: `https://my-discord-idle-bots.onrender.com`.

### Bước 4: Thiết lập UptimeRobot để chống Bot bị ngủ đông
Tài khoản Free trên Render sẽ tự động đi ngủ (sleep) sau 15 phút nếu không có traffic (lượt truy cập) nào gửi tới web server. Để giữ cho bot luôn thức 24/7:
1. Truy cập [UptimeRobot.com](https://uptimerobot.com/) và tạo tài khoản miễn phí.
2. Nhấp vào **Add New Monitor**.
3. Thiết lập thông số:
   - **Monitor Type**: Chọn `HTTP(s)`
   - **Friendly Name**: Đặt tên bất kỳ (ví dụ: `Discord Bots Keep-alive`)
   - **URL (or IP)**: Dán đường dẫn URL Render của bạn vào (ví dụ: `https://my-discord-idle-bots.onrender.com`).
   - **Monitoring Interval**: Chọn `Every 5 minutes` (mỗi 5 phút).
4. Nhấn **Create Monitor**. 
Bây giờ, cứ mỗi 5 phút UptimeRobot sẽ ping vào Web Server của bot trên Render một lần, giúp bot luôn thức và chạy 24/7 ổn định! 🎉
