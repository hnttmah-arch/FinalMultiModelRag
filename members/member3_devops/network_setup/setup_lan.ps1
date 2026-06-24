# Script PowerShell hỗ trợ thiết lập mạng LAN cho Node 2 (AI Inference Worker - Windows)
# Lưu ý: Bạn cần chạy PowerShell dưới quyền Administrator (Run as Administrator)

Write-Host "=== THIẾT LẬP FIREWALL & MẠNG LAN CHO NODE 2 ===" -ForegroundColor Green

# 1. Mở port cho API Gateway và Ollama
$ports = @(8001, 11434)
foreach ($port in $ports) {
    $ruleName = "Allow_DDM501_Port_$port"
    if (Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue) {
        Write-Host "Luật tường lửa cho Port $port đã tồn tại." -ForegroundColor Yellow
    } else {
        New-NetFirewallRule -DisplayName $ruleName -Direction Inbound -Action Allow -Protocol TCP -LocalPort $port
        Write-Host "Đã tạo luật tường lửa cho phép Port $port Inbound thành công." -ForegroundColor Cyan
    }
}

# 2. Hiển thị thông tin IP hiện tại để cấu hình IP tĩnh
Write-Host "`n=== THÔNG TIN IP ADAPTER HIỆN TẠI ===" -ForegroundColor Green
Get-NetIPAddress -InterfaceAddressFamily IPv4 | Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" } | Format-Table InterfaceAlias, IPAddress, IPv4Address -AutoSize

Write-Host "`nHướng dẫn đặt IP tĩnh trên Windows (Node 2):" -ForegroundColor Yellow
Write-Host "1. Mở Run (phím Windows + R), nhập 'ncpa.cpl' và nhấn Enter."
Write-Host "2. Nhấp chuột phải vào Adapter mạng đang kết nối LAN (ví dụ: Ethernet), chọn Properties."
Write-Host "3. Chọn 'Internet Protocol Version 4 (TCP/IPv4)' và bấm nút 'Properties'."
Write-Host "4. Chọn 'Use the following IP address' và điền địa chỉ IP tĩnh mong muốn (ví dụ: 192.168.1.100), Subnet mask (255.255.255.0) và Default gateway của Router."
Write-Host "5. Điền DNS (ví dụ: 8.8.8.8) và chọn OK để lưu."
