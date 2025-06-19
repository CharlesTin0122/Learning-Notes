# 概述
- 当程序运行时，你需要做一些初始化工作来进行相关设置，之后进入游戏主循环来让玩家持续玩下去。每一帧，你需要处理输入，更新游戏状态，并将结果渲染到屏幕上。当玩家退出游戏的时候，你需要清理并关闭程序。
```cpp
//游戏主线程
int main()
{
	//初始化设置
	init();
	//游戏主循环
	while(!g_exit_requested)
	{
		poll_input();//获取玩家输入
		game_update();//更新游戏
		render();//渲染到屏幕
	}
	shut_down();//清理并关闭游戏
}
```
- 在unreal engine中你并不会直接处理游戏循环。你会从定义一个GameMode子类并复写类似InitGame的方法。或者定义一个Actor或Component的子类，并复写他们的beginPlay()或者Tick()方法来添加自己的逻辑。你只需要做一些基本操作，引擎替你处理的所有的事情，这对刚开始制作游戏的人很方便，不过对于一个引擎的初学者也需要对引擎的游戏性框架有一个大概的了解。
![](attachments/UE游戏框架：从int%20main()到BeginPlay.png)
# 游戏的启动
- 游戏的启动是从Launch模块开始的，那里能找到多个为不同平台所定义的main函数，最终这些main函数都会进入Launch.cpp文件内的GuardedMain()函数。去除一些繁杂的代码，可以看到一个基本的游戏循环逻辑。

```cpp
#include "LaunchEngineLoop.h"


FEngineLoop GEngineLoop;//引擎的主要逻辑

bool GIsRequestingExit=false;

int32 GuardedMain(const TCHAR* CmdLine)
{
	// 早期初始化，加载引擎和游戏模块
	int32 ErrorLevel =GEngineLoop.PreInit(CmdLine);
	if(ErrorLevel!=0 || GIsRequestingExit)
	{
		return ErrorLevel;
	}
	
	//创建并初始化一个UEngine，执行后期初始化，启动游戏
	ErrorLevel = GEngineLoop.Init();
	
	//每帧更新游戏
	while(!GIsRequestingExit)
	{
		GEngineLoop.Tick();
	}
	
	// 清理并退出游戏
	GEngineLoop.Exit();
	return ErrorLevel;
}

```
- 引擎的主要循环逻辑是在一个叫FEngineLoop的类里面实现的。我们可以看到EngineLoop有一个PreInit阶段，在此之后引擎才完成初始化。之后就会每帧更新游戏状态，直到我们退出游戏。

## PreInit阶段

- `GEngineLoop.PreInit(CmdLine);`是大多数模块加载的地方，
	- 先加载引擎底层模块，这样就可以为基本系统进行初始化并定义一些基本类型。如果你的项目或者插件拥有在PreInit阶段加载的模块，那么接下来就会加载这些模块。
	- 之后加载高级引擎模块
	- 接下来就是Default阶段，项目和插件模块默认在这个阶段加载。这通常是你游戏的C++代码首次注入unreal engine实例的阶段。
	- 在基本的引擎功能加载并初始化之后，你的游戏模块也加载进来。但是此时还未生成游戏状态对象。
- 那么当模块加载时发生了什么？
	- 首先引擎会注册所有该模块中定义的UObject类，这使得反射系统能够发现这些类，同时还会为每个类构造一个类默认对象（Class Default Object简称CDO），CDO记录了这个类的默认状态。它还作为原型用于子类继承。所以如果你定义了一个Actor子类或者GameMode子类，或者是任何在前面用UCLASS宏标记的类型，EngineLoop会为这个类的默认实例分配空间。
	- 然后运行其构造函数，传入其父类的CDO作为模板，这就是构造函数不应该包含任何游戏性相关的代码的原因。它只是用于设定这个类的通用属性。而不是用来修改这个类的任何特定实例的。
	- 在所有的类注册完成之后，引擎调用模块的StartupModule方法，相对的还有ShutdownModule方法，让你可以处理任何与模块生命周期相关的初始化工作。
- 所以在这个阶段EngineLoop已经加载了所有需要的引擎，项目以及插件模块，还有这些模块中注册的类，以及所有必须的底层系统也会加载到位。至此PreInit阶段结束，接下来我们继续去执行Init方法。
## Init阶段

```cpp
int32 FEngineLoop::Init()
{
	// 1.Load the UGameEngine class that's specified in the Engine config file
	FString GameEngineClassName;
	GConfig->GetString(TEXT("/Script/Engine.Engine"),TEXT("GameEngine"),GameEngineClassName.GEngineIni);
	EngineClass = StaticLoadclass(UGameEngine::Staticclass(),nullptr,*GameEngineClassName);
	
	// 2.Create a new UGameEngine and enshrine it as the global UEngine object
	GEngine =NewObject<UEngine>(GetTransientPackage(),Engineclass);
	check(GEngine);
	
	//3.Initialize the engine: this creates UGameInstance and UGameViewportClient
	GEngine->ParseCommandline();
	GEngine->Init(this);
	FCoreDelegates::0nPostEngineInit.Broadcast();
	
	//4.Initialize any late-loaded modules
	IProjectManager::Get().LoadModulesForProject(ELoadingPhase::PostEngineInit);
	IPluginManager::Get().LoadModulesForEnabledPlugins(ELoadingPhase::PostEngineInit);
	
	//5.Start the game:typically this loads the default map
	GEngine->Start();
	GIsRunning = true;
	FCoreDelegates::0nFEngineLoopInitComplete.Broadcast();
	return 0;
}

```

- EngineLoop的Init方法相对比较简单直白，他将事情交给名为UEngine的类来处理。unreal engine 包含一个名为Engine的模块（UE_4.25/Engine/Source/Runtime/Engine），在该模块中有一个名为Engine.h的头文件，在这头文件中定义了一个UEngine的类，并衍生为UEditEngine和UGameEngine两个类。
1. 在游戏的整个Init阶段，FEngineLoop检查了Engine配置文件来找出使用哪个GameEnine类。
2. 接着创建该类的实例，并让全局UEngine类型指针来指向他，从而可通过在Engine/Engine.h中声明的全局变量GEngine来访问它。
3. 当Engine实例被创建并初始化之后，EngineLoop出发一个全局委托来告知引擎现在已经初始化了。
4. 接下来就会加载那些设置在PoseEngineInit阶段加载的插件和项目模块。
5. 最后引擎就正式启动了，初始化工作也完成了。
## 加载地图
- 那么Engine类实际上是做什么的呢？他要做很多事情，包括Browse和LoadMap方法。我们经过一个启动过程并初始化了所有引擎系统，但是要进入实际游戏还得加载一张地图。而UEngine这个类会负责这个任务。
- Engine对象能够浏览一个URL，这个URL可以代表一个要作为客户端连接的服务器地址或者是本地加载的地图名称。URL后面还能添加相应参数。
- 当你在项目的DefaultEngine.ini文件里设置一张默认地图的时候，你是在告诉引擎在启动后自动浏览至这张地图。在打包项目为development builds类型时，你可以通过在命令行添加URL来覆盖默认地图。你也可以在游戏运行的时候打开控制台使用Open URL命令来浏览至指定地图。
### Engine的初始化流程

```cpp
void UGameEngine::Init(IEngineLoop* InEngineLoop)
{

	UEngine::Init(InEngineLoop);
	//一个GameInstance对象
	FSoftClassPath GameInstanceClassName = GetDefault<UGameMapsSettings>()->GameInstanceClass;
	UClass* GameInstanceClass = LoadObject<UClass>(NULL, *GameInstanceClassName.ToString()
	GameInstance = NewObject<UGameInstance>(this, GameInstanceClass);

	GameInstance->InitializeStandalone();


	// 一个GameViewportClient对象
	UGameViewportClient* ViewportClient = NewObject<UGameViewportClient>(this, GameViewportClientClass);;
	ViewportClient->Init(*GameInstance->GetWorldContext(), GameInstance);
	GameViewport = ViewportClient;
	GameInstance->GetWorldContext()->GameViewport = ViewportClient;
	CreateGameViewport( ViewportClient );
	
	//一个LocalPlayer对象
	FString Error;
	ViewportClient->SetupInitialLocalPlayer(Error);
	UGameViewportClient::OnViewportCreated().Broadcast();

	UE_LOG(LogInit, Display, TEXT("Game Engine Initialized.") );
	bIsInitialized = true;
}
```
- Engine会在地图加载完之前进行初始化，而在初始化过程中会创建一些重要对象：
	- 一个GameInstance对象
	- 一个GameViewportClient对象
	- 一个LocalPlayer对象
- 你可以认为LocalPlayer对象代表坐在屏幕前的用户。而GameViewportClient对象可以当做屏幕本身，他本质上就是作为渲染，声音以及输入系统的高级接口，也即是用户和引擎之间的交互接口。
- UGameInstance类是到UE4.4版本才出现的类型，它被从UGameEngine类中剥离出去，来处理一些原本由Engine对象来处理的特定于项目的功能。所以在Engine初始化之后，我们拥有了一个GameInstance，一个GameViewportClient对象，一个LocalPlayer对象
- 这一步完成之后游戏就可以启动了。
- `GEngine->Start();`这里就是首次调用LoadMap方法的地方，在调用之后，我们将有用一个UWorld对象来包含所有保存在游戏地图中的Actor，之后我们还将生成构成GameFramework核心的一系列Actor对象：包括一个GameMode，GameSession，GameState，GameNetworkMannager，PlayerController，PlayerState以及一个Pawn对象。
- 这两组对象的主要区别就是他们的生命周期。从高层系统上来说，需要两种生命周期：
	- 地图加载之前就存在的对象：
		- UGameEngine，UGameInstance，UGameViewportClient，ULocalPlayer
	- 地图加载之后才生成的对象：
		- UWorld，ULevel，UActorComponent
		- AActor，AGameModeBase，AGameSession，AGameStateBase，AGameNetworkMannager，APlayerController，APlayerState,Apawn
![](attachments/UE游戏框架：从int%20main()到BeginPlay-2.png)
- 地图加载之后才生成的对象只会和你当前游玩的地图一同存在。当然引擎支持一种叫做“seamless travel”的方法来让你在转移到新地图的时候保留部分对象。但如果你直接切换到新地图，或者链接到其他服务器，或退出到主菜单，那么所有Actor对象都会被销毁，World会被清空，这些类的对象也不复存在，直到你加载下一张地图。
### LoadMap
- 来看看LoadMap方法里面发生了什么
	- 引擎会先触发一个全局委托来表明游戏地图就要更换了
	- 如果当前已经加载了一张地图，他会清理并销毁当前的World
	- 运行到这里时还不存在一个World，我们只有一个world上下文对象，这个对象在初始化过程中由GameInstance生成，他本质上是一个永久对象，用于追溯当前加载的World。在加载任何对象之前，GameInstance可以预先加载他想要的资源，但是默认情况下它什么也不做。
	- 接下来我们需要一个UWorld对象，如果你在编辑器内编辑地图，那么编辑器其实已经将UWorld对象连同一个或多个包含你放置的Actor的ULevel对象一起加载到内存里了。当你在永久保存关卡时，当前世界和他内部的关卡以及它所有的Actor对象都会背序列化到一个地图Package对象里，该Package对象会被写入到磁盘上的.umap文件中。所以在执行LoadMap过程中，引擎会找到这个地图的package并加载。
	- 这时World和它的永久关卡极其所有的Actor对象，包括WorldSettings对象一一都会被加载到内存中。
	- 既然我们有一个World，那么就要对其初始化了
		- 引擎在World中保存了对GameInstance的引用，然后初始化GWorld变量来引用这个World对象。
		- 接下来这个World对象的引用会保存到WorldContext中，并将其世界类型设置为Game。在这里他会调用AddToRoot方法，放置被垃圾回收。
		- InitWorld方法会让World对象能对一些像是物理，寻路导航，AI以及声音系统进行设置。
		- 当我们调用SetGameMode时，World对象会让GameInstance在世界生成一个GameMode的Actor对象。
		- 当GameMode生成之后，引擎会加载地图，同时它所有被设置为永久加载的子关卡及其被引用的资产也会被加载。
		- 下一步就是InitializeActorForPlay，这里就是创造游戏世界的地方。在这里World对象会对所有Actor对象进行几次循环遍历
			- 第一次循环会注册世界中所有的Actor组件，每一个Actor内的每一个组件都要注册，注册一个组件要做三件事
				- 首先将所属的World的引用保存到组件中。然后调用组件的OnRegister函数，从而可以做一些初始化早期工作。同时如果该组建是一个PrimitiveComponent，那么除了上述这些，在注册完成之后这个组件会创建一个FPrimitiveSceneProxy，并添加到FScene中，FScene相当于渲染线程版本的UWorld。一旦组件被注册之后，World对象会调用GameMode的InitGame方法，该方法内GameMode会生成一个GameSession类的Actor对象。之后就是下一个循环。
				- 这里world会让每一个关卡来初始化自己所有的Actor。在这里会遍历两次，