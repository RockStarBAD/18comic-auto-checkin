需配置GitHub Secrets:   USER_AGENT、COOKIE、USERNAME、PASSWORD

目前没法绕过 Cloudflare，即该项目暂时无效等待修改代码 --------------已可绕过Cloudflare

自动登录可以但是自动签到不行，等待更正代码

尝试修改签到逻辑:首先查找并点击元素"每日簽到"，点击后会弹出界面，在这个新的界面（应当出现在屏幕正中）有两个按钮，一个是"簽到",旁边一个是"關閉",这个时候再点击"簽到"完成签到----代码修改完成但是运行失败，始终出现
Run python checkin.py
  
Traceback (most recent call last):
  File "/home/runner/work/18comic-auto-checkin/18comic-auto-checkin/checkin.py", line 121, in <module>
    main()
    ~~~~^^
  File "/home/runner/work/18comic-auto-checkin/18comic-auto-checkin/checkin.py", line 102, in main
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
TypeError: WebDriver.__init__() got multiple values for argument 'options'
Error: Process completed with exit code 1.       
  一类的错误

  因为我完全不懂代码，一切靠chatgpt实现，而只要一修改签到逻辑就会出现类似这种的错误，我还不能保证这样的签到逻辑代码就能完成签到，基本上放弃了，如果后续有大佬看到这个项目并实现了自动签到可以pull requests。。。。
