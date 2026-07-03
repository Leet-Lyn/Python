# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 在脚本开始前让我选择：1. Torrents 文件夹写入 Magnet 数据库；2. 多行 Magnet 链接写入数据库；3. 多行 Magnet 链接从数据库删除；4. 多行 Magnet 值从数据库删除；5. 整理数据库；0. 退出。
# 1. Torrents 文件夹写入 Magnet 数据库：
# 询问我源文件夹位置（默认为：d:\Studios\Folders\Downloads\）。 写入文件夹位置（默认为：d:\Studios\Folders\Ins\）, 删除文件夹位置（默认为：d:\Studios\Folders\Deletes\）。Magnet 数据库文件位置（默认为：e:\Documents\Softwares\Codes\Attachments\Databases\Magnet\Magnet.txt）。
# 遍历源文件夹内所有 torrent 文件及子文件夹中的 torrent 文件，顺序完成。
# 将 torrent 提取出 Magnet 链接（Hex 格式），导出其 40 位十六进制（SHA-1 Hash），为 Magnet 值。
# 比对 Magnet 数据库文件（Magnet 数据库文件，每一行为一个文件的 Magnet 值。）如果当前文件的 Magnet 值在原来 Magnet 数据库文件里存在，则将该文件移动到删除文件夹，选择下一个文件。
# 如果当前文件的 Magnet 值不在原来 Magnet 数据库文件里存在，则添加该文件的 Magnet 值到 Magnet 数据库文件末尾（另起一行），保存 Magnet 数据库文件。将该torrent 文件安装文件夹子文件夹结构，移动到写入文件夹位置，
# 直至源文件夹内所有文件及子文件夹中的文件都处理好结束。最后整理哪些文件 Magnet 值原数据库存在，移动到删除文件夹里。并将这些文件列表打印在屏幕上并复制到剪贴板上去。
# 2. 多行 Magnet 链接写入数据库：
# 询问我 Magnet 数据库文件位置（默认为：e:\Documents\Softwares\Codes\Attachments\Databases\Magnet\Magnet.txt）。读取剪贴板数据，其为多行 Magnet 链接（每行一个 Magnet 链接），顺序读取每一行 Magnet 链接，（如非 Hex 格式的链接转成 Hex 格式的链接）。导出其 40 位十六进制（SHA-1 Hash），为 Magnet 值。
# 比对 Magnet 数据库文件（Magnet 数据库文件，每一行为一个文件的 Magnet 值。）
# 如果当前 Magnet 值在原来 Magnet 数据库文件里存在，报告我。
# 如果当前 Magnet 值不在原来 Magnet 数据库文件里存在，则添加该 Magnet 值到 Magnet 数据库文件末尾（另起一行），保存 Magnet 数据库文件。
# 最后整理哪些 Magnet 链接的 Magnet 值原数据库存在。并将这些文件列表打印在屏幕上并复制到剪贴板上去。
# 3. 多行 Magnet 链接从数据库删除：
# 询问我 SizeMD4 数据库文件位置（默认为：e:\Documents\Softwares\Codes\Attachments\Databases\Magnet\Magnet.txt）。读取剪贴板数据，其为多行 Magnet 链接（每行一个 Magnet 链接），顺序读取每一行 Magnet 链接，（如非 Hex 格式的链接转成 Hex 格式的链接）。导出其 40 位十六进制（SHA-1 Hash），为 Magnet 值。
# 比对 Magnet 数据库文件（Magnet 数据库文件，每一行为一个文件的 Magnet 值。）
# 如果当前 Magnet 值在原来 Magnet 数据库文件里存在，则将该 Magnet 值从原来 Magnet 数据库文件里删除。
# 如果当前 Magnet 值不在原来 Magnet 数据库文件里存在，则报告我。
# 4. 多行 Magnet 值从数据库删除：
# 询问我 Magnet 数据库文件位置（默认为：e:\Documents\Softwares\Codes\Attachments\Databases\Magnet\Magnet.txt）。读取剪贴板数据，其为多行 Magnet 值（每行一个 Magnet 值），顺序读取每一行 Magnet 链接，（如非 Hex 格式的链接转成 Hex 格式的链接）。导出其 40 位十六进制（SHA-1 Hash），为 Magnet 值。
# 比对 Magnet 数据库文件（Magnet 数据库文件，每一行为一个文件的 Magnet 值。）
# 如果当前 Magnet 值在原来 Magnet 数据库文件里存在，则将该 Magnet 值从原来 Magnet 数据库文件里删除。
# 如果当前 Magnet 值不在原来 Magnet 数据库文件里存在，则报告我。
# 5. 整理数据库：
# 询问我 Magnet 数据库文件位置（默认为：e:\Documents\Softwares\Codes\Attachments\Databases\Magnet\Magnet.txt）。对 Magnet 数据库，先备份，再对文件里的 Magnet 值（字符串）从小到大排序。
# 完成后，反复循环至最开始。

# 导入模块