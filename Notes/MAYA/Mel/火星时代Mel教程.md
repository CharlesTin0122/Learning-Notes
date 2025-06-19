p2，selected命令：

```
select pSphere1;
```

```
select group2|pSphere1;
```

p3，print命令：

```
print("hello world");
```

```
select pSphere1;print("I select the pSphere1!") ;
```

```
//双斜杠表示注释，不会执行。\n表示换行.
select pSphere1;
print("I select pSphere1!\n");
print("pSphere1 is ready!")
```

p6,system命令;

```
//打开记事本软件，注意斜杠方向
system("start C:/Windows/notepad.exe")
```

p8,file命令：

```
//-force是执行，-newFile创建新场景
file -force -newFile；
```

//设置文件名称，保存文件并指定文件类型

```
file -rename "new1.ma";
file -save -type "mayaAscii";
```

p9,变量：

```
//integer整数,$变量,这里print不用双引号
int $MyFirstInt;
$MyFirstInt=1;
print($MyFirstInt);
```

```
//float浮点,$变量
float $MyFirstfloat;
$MyFirstfloat=3.14;
print($MyFirstfloat);
```

```
//string字符串,$变量
string $MyFirststring;
$MyFirststring="maya";
print("this is may first string "+$MyFirststring);
```

p11,递增保存文件：

```
int $counter;
$counter=$counter+1;
print($counter);
print("\n");
file -rename ("test"+$counter+".ma");
file -s -type "mayaAscii";
print("Just Saved "+("test"+$counter+".ma"))
```

p12,设置属性setAttr

```
setAttr "pCube1.rotateZ" 60;
float $a=5;
setAttr "pCube1.rotateZ" $a;
```

p13,获取属性：getAttr

```
float $Charles;
$Charles=getAttr "pCube1.rotateZ";
print($Charles);
float $Tin;
$Tin=$Charles+30;
setAttr "pCube1.rotateZ"$Tin;
```

p14,if else语句

```
string $myrender=getAttr defaultRenderGlobals.currentRenderer;
print($myrender);
print("\n");
if($myrender=="arnold"){
print("right");
}else{
print("Wrong");
}
```

p19,数组

//数组内包含五个整数分别是2,6,9,7,5，打印第三个整数

```
int $myArray[5];
$myArray={2,6,9,7,5};
print($myArray[2])
```

p21，for in循环：设立字符串数组，将所有选择的物体加入数组，打印这些物体的名称并Y轴移动30，（ls -sl;前后加单引号）

```
string $objsel[]=`ls -sl`;
for($myObject in $objsel){
print($myObject+"\n");
setAttr ($myObject+".translateY")30;
}
```

p24,窗口布局

```
if(window -exists $window){
deleteUI -window $window;
}
string $window=window -title "key"                        -widthHeight 200 500                        mywindow;
rowColumnLayout -numberOfColumns 2 -columnWidth 1 30;
symbolButton -image"hand.cur";text -label "  TanslateX";
symbolButton -image"hand.cur";text -label "  TanslateY";
symbolButton -image"hand.cur";text -label "  TanslateZ";
symbolButton -image"rotate.cur";text -label "  RotateX";
symbolButton -image"rotate.cur";text -label "  RotateY";
symbolButton -image"rotate.cur";text -label "  RotateZ";
symbolButton -image"zoom.cur";text -label "  ScaleX";
symbolButton -image"zoom.cur";text -label "  ScaleY";
symbolButton -image"zoom.cur";text -label "  ScaleZ";
showWindow;
```

p28,KeyFrame小工具

```
//creat the proc;
proc keyer(int $choose){
    string $sel[]=`ls -selection`;
    for($myObject in $sel){
        if($choose==1) setKeyframe -attribute "translateX";
        if($choose==2) setKeyframe -attribute "translateY";
        if($choose==3) setKeyframe -attribute "translateZ";
        if($choose==4) setKeyframe -attribute "rotateX";
        if($choose==5) setKeyframe -attribute "rotateY";
        if($choose==6) setKeyframe -attribute "rotateZ";
        if($choose==7) setKeyframe -attribute "scaleX";
        if($choose==8) setKeyframe -attribute "scaleY";
        if($choose==9) setKeyframe -attribute "scaleZ";
    }
}
//creat the window
if(`window -exists $window`){
    deleteUI -window $window;
}
string $window=`window -title "key"
                       -widthHeight 200 500
                       mywindow`;
rowColumnLayout -numberOfColumns 2 -columnWidth 1 30;

symbolButton -image"hand.cur";-command "keyer(1)";text -label "  TanslateX";
symbolButton -image"hand.cur";-command "keyer(2)";text -label "  TanslateY";
symbolButton -image"hand.cur";-command "keyer(3)";text -label "  TanslateZ";


symbolButton -image"rotate.cur";-command "keyer(4)";text -label "  RotateX";
symbolButton -image"rotate.cur";-command "keyer(5)";text -label "  RotateY";
symbolButton -image"rotate.cur";-command "keyer(6)";text -label "  RotateZ";


symbolButton -image"zoom.cur";-command "keyer(7)";text -label "  ScaleX";
symbolButton -image"zoom.cur";-command "keyer(8)";text -label "  ScaleY";
symbolButton -image"zoom.cur";-command "keyer(9)";text -label "  ScaleZ";

showWindow;
```

p31,for循环

```
for($i=0;$i<10;$i++){
    for($j=0;$j<10;$j++){
    polyCube;
    move -relative $j 0 $i;
    print($i+"  ");
    print($i+"\n"); 
   }
}
   
```

P30,批量选中物体建立父子关系

```
string $sel[]=`ls -selection`;
for($j=1;$j<size($sel);$j++){
    string $CurrObj=$sel[$j];
    string $PrevObj=$sel[$j-1];
    parent $CurrObj $PrevObj;
}
```

p35,递增保存

```
//query:询问,sceneName:显示路径和名称，shortName：只显示文件名 
//substituteAllString替换字符
//match：匹配字符，后者与前者匹配的被提取
string $fileName=`file -query -sceneName -shortName`;
$fileName=substituteAllString($fileName,".mb","");
$fileName=substituteAllString($fileName,".ma","");
string $stringNumber=`match "[0-9]+" $fileName`;
int $n;
if($stringNumber==""){
    $n=1;
}else{
    $n=$stringNumber;
    $n=$n+1;
    $fileName=substituteAllString($fileName,$stringNumber,"");
}

file -rename ($fileName+$n);
file  -save -type "mayaAscii";
print("Just Saved "+($fileName+$n))
```

p38,locator控制灯光

```
//connectAttr连接属性
select -r locator1 ;
addAttr -ln "control_light_intensity"  -at double  -dv 0 
addAttr -longName "controlColor" -usedAsColor -attributeType float3;
addAttr -longName "red" -attributeType "float" -parent "controlColor";
addAttr -longName "blue" -attributeType "float" -parent "controlColor";
addAttr -longName "green" -attributeType "float" -parent "controlColor";

select -r pointLight2 pointLight4 pointLight3 pointLight1
string $sel[]=`ls -selection`;
for($myobject in $sel){
    connectAttr -force locator1.controlColor ($myobject+".color");
    connectAttr -force locator1.control_light_intensity ($myobject+".intensity");
}
```

p39,python

```python
import maya.cmds
maya.cmds.polySphere()
maya.cmds.select("pSphere2")
print"Charles"
```