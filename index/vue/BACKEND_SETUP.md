# 后端服务器网络访问配置

## 问题诊断

当前后端服务器只监听 `127.0.0.1:5251`，这意味着只能从本机访问。为了支持手机等其他设备访问，需要配置后端服务器监听所有网络接口。

## 解决方案

### 如果是Flask应用
```python
# 修改Flask应用启动代码
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5251, debug=True)
```

### 如果是FastAPI应用
```python
# 修改uvicorn启动配置
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5251, reload=True)
```

### 如果是Django应用
```bash
# 使用命令行启动
python manage.py runserver 0.0.0.0:5251
```

### 如果是Node.js/Express应用
```javascript
// 修改服务器启动代码
const port = 5251;
app.listen(port, '0.0.0.0', () => {
    console.log(`Server running on http://0.0.0.0:${port}`);
});
```

## 验证配置

1. 重启后端服务器
2. 运行以下命令检查监听状态：
   ```bash
   netstat -an | findstr :5251
   ```
3. 应该看到类似这样的输出：
   ```
   TCP    0.0.0.0:5251         0.0.0.0:0              LISTENING
   ```

## 防火墙配置

如果仍然无法访问，可能需要配置防火墙：

### Windows防火墙
1. 打开Windows防火墙设置
2. 选择"允许应用或功能通过Windows防火墙"
3. 添加端口5251的入站规则

### 或者使用命令行
```bash
netsh advfirewall firewall add rule name="Backend API" dir=in action=allow protocol=TCP localport=5251
```

## 测试访问

### 本地测试
```bash
curl http://localhost:5251/api/hot
```

### 网络测试（从其他设备）
```bash
curl http://[你的电脑IP]:5251/api/hot
```

## 当前前端配置

前端已配置为智能检测后端地址：
- 开发环境：通过Vite代理访问 `/api/*`
- 手机访问：代理会尝试连接到本地后端服务
- 如果代理失败，会返回明确的错误信息

## 故障排除

1. **端口占用**: 确保5251端口没有被其他服务占用
2. **防火墙**: 确保防火墙允许5251端口访问
3. **网络**: 确保所有设备在同一网络下
4. **后端绑定**: 确保后端服务绑定到0.0.0.0而不是127.0.0.1
