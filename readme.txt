该脚本是基于topRobot修改
修改点如下：
1. 因为U4和chrome无法使用浏览器的截屏功能，改为调用android系统的截屏功能
2. 注释掉实时上传的调用，因为有时会卡死
3. 优化了php-server/index.php文件，使页面每行仅展示2张图片，方便对比查看
4. 如果需要每行显示多张图片，可自行修改php文件

跑出结果后，需要人工干预：
#跑出来的截屏图片在client/pics，将pics中的文件打包上传到服务器的php-server中sites目录下
#同时将php-server/index.php也拷入图片目录

跑出来的截屏图片在client/pics
本地搭建有lamp环境时，将该文件夹拷贝到本地apache目录下，同时将php-server/index.php拷贝到图片目录
index.php会读取当前目录下的文件展示
