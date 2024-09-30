# POP3-Email-Transimit-Receiver
Mail sending and receiving function based on POP3 protocol (there are many different interfaces)

## `EmailReceiver`类具有以下方法

- `get_emailbox_state() -> tuple` 
- 获取邮箱当前邮件数与总字节数，输出与 POP3 服务器的交互信息

- `pop_connect()`
- 通过 SSL 连接至 POP3 服务器

- `get_attachment_content(email_index)`
- 获取邮件中的所有附件，并保存在根路径中

- `get_content(email_index)`
- 获取邮件未解码内容，并存储至 Email Content.txt

- `get_email_head_info(email_index) -> tuple`
- 获取邮件头信息（From、To、Date、Subject）

- `get_text_content(email_index) -> str`
- 获取邮件正文的文本内容（非HTML格式）

- `get_email_list() -> None`
- 列出邮箱内所有的邮件，输出至终端

## CommandReceiver 类具有以下方法

- `do_specific_command(command: str) -> None`
-  通过 OS 库对命令行进行调度，判断各种不同的情况
	- close：关机
	- reset：重启
	- VPN：关闭AnyConnct VPN
	- Sunshine：运行指定的 Sunshine.pyw 脚本

## EmailSender 类具有以下方法
- `stmp_connect()`
- 通过 SSL 连接至 STMP 服务器

- `open_stmp_debug()`
- 开启与 STMP 的交互，实时获取返回的信息

- `stmp_send_text_email()`
- 通过 STMP 服务器发送纯文本邮件

- `stmp_send_attachment_email()`
- 通过 STMP 服务器发送带附件邮件

## Study Information
IMAP 和 POP 有什么区别？  
POP 允许客户端下载服务器上的邮件，但是你在电子邮件客户端上的操作（如：移动邮件、标记已读等）不会反馈到服务器。
IMAP 协议中，客户端的操作都会反馈到服务器，对邮件进行的操作（如：移动邮件、标记已读、删除邮件等）服务器上的邮件也会做相应的动作。
同时，IMAP 可以只下载邮件的主题。


