# 记录

### 2023年12月24日22点38分：

真是服了，搞了两天怎么记录输入，但根本没有效果。

现在的情况是直接使用IME的API根本获取不到上下文，但有个csdn上的很复杂的程序的结果显示是可以的。

有两种可能的情况，一是overflow和知乎上说的那样，IME它不支持跨线程调用，因此需要全局hook，但是我又不会windows的hook，gpt4还不给写；二是这个IME是很早之前的，有一些帖子说现在变成TFS了，原来的不能用了在win10里面。

对于第一种情况，解决方法可能是把csdn上的那个玩意考下来问问gpt怎么运行，或者自己写一个；对于第二种方案，gpt给不了TFS的信息，windows官网也没有实例，真是服了。另外还看到说用更老的API可以；还有第三种方法，查查有没有提供记录的常见输入法，但这种不太现实，因为但凡大点的输入法都会考虑安全隐私问题不会记录。

现在姑且先收集着活动窗口标题把，自动写readme可能不太现实，但搞个“滚去学习”提醒器应该还是可以的。

现在的活动标题记录是用死循环写的，后续可能改成触发式？好像也不大好改，windows这边实在是一窍不通。

### 2023年12月25日11点27分：

mac上的活动窗口记录搞定了，用的appscript脚本，api完全不可用

mac上输入法更复杂了，根本没有api，就先这样吧

接下来的计划是先实现提醒功能算了。在mac上不能用虚拟桌宠，还要自己实现下tts和基础交互，好烦。

```
你是一个ai助手，你需要以第二人称的格式返回结果用于与用户对话。你的语气应该比较生动活泼，不要像程序一样过于规整。你有很多功能，但一次只能激活一个功能，注意，仅激活一个！！功能的激活有优先级，优先激活排在前面的功能，一个功能激活后就不要输出另一功能的结果了！！！
你有功能1，每隔几秒程序会发送给你用户活动窗口记录，你需要根据时间判断用户是不是长时间进行娱乐项目，当监测到时提醒用户，这个时间先设置为30分钟秒。请以较为严厉的语气提醒，句子应该很短；
你有功能2，根据上面的记录，你要通判断用户刚刚在做什么，并从用户感兴趣的主题中随机挑选一个进行进一步讨论，最好使用疑问句来进行，注意是仅挑选一个，这个功能的输出不要过于专业，句子不要过长；
```

用上面的这种进行测试发现他还是会同时进行两功能，然后并不能清晰认识到时间概念。感觉还是要分开，然后人为控制任务。

### 2023年12月26日12点07分：

搞定了初版assistent实现的自动调度，现在包含查文件、掉函数的基本功能。

函数包含的功能有联网查询（google api）、图片生成（dalle api）、查表（本地数据）
同时写了个edge-tts的函数，还没有整合进去。
这里好像不用整合进去，这个东西应该是在大循环里面的？
不对不对，要整合进去，否则会输出出来一些不用输出的东西。

关于tts，看到有音色模拟的模型，训练好就可以和正常tts一样实时生成了，回来跟lbw要来模型看看能不能运行起来。

下一步要要把循环逻辑写出来了，实现主动对话功能；
然后是试一下longchain，assistent这边每次加新功能都要重新创建assistent，就很贵。。。
再加一个，试一下连环调用，就是根据一个调用的结果调用另一个。

### 2023年12月26日17点30分：

循环逻辑还没写

langchain试了，暂时感觉没有assistent好用，可能是懒惰心作祟吧，仔细想的话还是longchain好用一点，因为可以自定义分类模型的温度等参数。

但是消耗有点大，毕竟是不停把输出传进去，会成倍增加。
assisent那边就好一点，他只记录一次，虽然每次调用assistent还要单独收费。
哦对，文件也要。。。

连环调用，根本不用自己写，他会很主动得连续调用（tts后画幅图安慰下什么。。。）
所以又觉得langchain调整灵敏度会好一点。

接下来还是先写逻辑循环，主要要权衡下要不要分离下管活动记录的和管正常交互的。这里ai自己分开总是有点问题，但不分开又没办法连续对话了。

或许可以每次开个主题就开个thread？好像可以