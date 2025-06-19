1.3命令结构

```
//创建
polySphere -r 1;
//查询
polySphere -q -r pSphere1;
//编辑
polySphere -e -r 2 pSphere1;
```

1.5数组

```
string $list[];
$list={"1","2","3"};
$list[0]="0";
print($list);
size($list);
```

1.6条件语句

```
//<,>,<=,>=,==,!=
int $a=1;
int $b=0;
if($a=$b){
    print dengyu;
}else{
    print budengyu;
}
```

```
int $i;
for($i=0;$i<100;$i++){
    polySphere;
    setAttr ("pSphere"+($i+1)+".translateX") (rand(-10,10));
    setAttr ("pSphere"+($i+1)+".translateY") (rand(-10,10));
    setAttr ("pSphere"+($i+1)+".translateZ") (rand(-10,10));
}
```

```
string $selObj[]=`ls -sl`;
for($ct in $selObj){
    setAttr ($ct+".translateX") (rand(-10,10));
    setAttr ($ct+".translateY") (rand(-10,10));
    setAttr ($ct+".translateZ") (rand(-10,10));
}
```

```
//continue意为跳过
for($str in{"1","2","3"}){
    if($str=="2"){
        continue;
}        
        print $str;
        print "\n";
}
```

1.8函数

```
proc string[] test_proc(string $s,string $n){
    print($s);
    print(">>>");
    print($n);
    return {">>>","<<<"};
}
test_proc("A","B");
```

```
global proc BJDX(float $a,float $b){
    if($a>$b){print($a+" is bigger");}
    else if($a==$b){print("same!");}
    else {print($b+" is bigger");}
}
BJDX 3.14 3.15;
```

```
proc ct_rigNodes(int $cons){
    string $sel[]=`ls -sl`;
for($obj in $sel){
    string $cir[]=`circle`;
    matchTransform $cir[0] $obj;
    if($cons==1){
    parentConstraint $cir[0] $obj;
    }
  }
}
ct_rigNodes(1);
```

1.9字符串操作

```
string $test="sl";
print $test;

string $test="sl\"";
print $test;

string $test="sl\\";
print $test;

string $test="sl\nsl";
print $test;

string $test="sl\tsl";
print $test;

string $test="sl\\tsl";
print $test;
```

```
//tokenize分割字符串
string $list[];
tokenize "25.25" "." $list;
print $list;
```

1.10常用命令

```
//ls返回名称，-sl-选择，-fl-显示每个元素名称
ls -sl -fl;
```

```
//size返回数量
string $ct_size[]={"1","2","3"};
size($ct_size)
```

```
//范利
string $sel[]=`ls -sl`;
for($i=0;$i<size($sel);$i++){
    print($i+"\n");
}
```

```
//位置信息,调整目标位置为000
xform -t 0 0 0 pSphere1;
```

```
//查询目标位置
xform -q -t pSphere1;
```

```
//获取属性
getAttr pSphere1.visibility;
//设置属性
setAttr pSphere1.visibility 1;
```

```
//查询层级关系，默认是获得子物体名称
listRelatives;
//查询层级关系，获得父物体名称
listRelatives -p;
//查询层级关系，获得子物体名称
listRelatives -c;
//查询所有子物体
listRelatives -ad;
```

```
//查询输入链接和输入链接对象
listConnections -c on;
```

```
//查询目标是否存在
objExists("pSphere1");
//查询目标类型
objectType("pSphereShape1");
```

```
//动态执行代码
eval("polySphere -r 1 -sx 20 -sy 20 -ax 0 1 0 -cuv 2 -ch 1;")
```

1.11两个模型之间传递点位置案例

```
string $sel[]=`ls -sl`;
string $sel_out_mesh=$sel[0];
string $sel_in_mesh=$sel[1];
select -r ($sel_out_mesh+".vtx[*]");
int $size=size(`ls -sl -fl`);
for($i=0;$i<$size;$i++){
    float $pos[]=`xform -q -t ($sel_out_mesh+".vtx["+$i+"]")`;
    xform -t $pos[0] $pos[1] $pos[2] ($sel_in_mesh+".vtx["+$i+"]");
}
```

2.4创建窗口

```
//-adj on窗口对齐，flowLayout横向布局，columnLayout纵向布局
window -title "myWindow" -widthHeight 200 100;
    string $flow=`flowLayout`;
        string $col=`columnLayout -adj on -p $flow`;
            button -label "traslationX" -p $col;
            button -label "traslationY"-p $col;
            button -label "traslationZ"-p $col;
        $col=`columnLayout -adj on -p $flow`;
            button -label "rotatX" -p $col;
            button -label "rotatY"-p $col;
            button -label "rotatZ"-p $col;
        $col=`columnLayout -adj on -p $flow`;
            button -label "scaleX"-p $col;
            button -label "scaleY"-p $col;
            button -label "scaleZ"-p $col;            
showWindow;
```

```
//保持窗口刷新
if(`window -exists mywindow`){
    deleteUI mywindow;
}
//新建窗口
window -title "window" -widthHeight 360 240 mywindow ;
//创建行式布局,按钮撑满布局
columnLayout -adjustableColumn true;
text -label "\n Creat Object \n";
//创建滑动条
floatSliderGrp -label "半径" -field true -min 0.01 -max 30.0 fsg01;
//创建按钮
button -label "Sphere" -c mySphere;
button -label "Cube" -c polyCube;
button -label "Plane" -c polyPlane;
//显示窗口
window -e -wh 360 240 mywindow;
showWindow mywindow;
//创建球半径函数
global proc mySphere(){
    float $Ra=`floatSliderGrp -q -value fsg01`;
    polySphere -radius $Ra;
}
```

2.5对话框

```
//confirmDialog确认对话框
string $conf=`confirmDialog -title "confirmDialog" -message "chose the button"
    -button "yes" -button "no"`;
print $conf;
```

```
//promptDialog 输入对话框
string $text="";
string $resul=`promptDialog -title "promptDialog" -message "input:"
                             -button "Yes" -button "No"`;
if($resul=="Yes"){
    $text=`promptDialog -query -text`;
}
print $resul;
print $text;
```

```
//fileDialog2 保存对话框
string $fileDialog2[]=`fileDialog2 -fileFilter "*.mb;;*.ma" -dialogStyle 2`;
```

2.6maya事件

```
//此命令创建一个“脚本作业”，该命令是MEL命令或脚本。每当条件切换到所需状态（或触发触发器等）时，脚本都会运行.
int $jobNum=`scriptJob -conditionTrue "playingBack" "print `currentTime -q`;" -protected`;
//退出当前作业脚本
scriptJob -force -kill $jobNum;
```

```
int $jobNum=`scriptJob -attributeChange "pSphere1.tx" "print `getAttr pSphere1.tx`;" -protected`;

scriptJob -force -kill $jobNum;
```

2.7约束工具

```
global proc ct_selconA(){
    string $sel[]=`ls -sl`;
    textField -e -text $sel papaObj1;
}

global proc ct_selconB(){
    string $sel[]=`ls -sl`;
    textField -e -text $sel sonObj1;
}
global proc ct_selconC(){
    string $sel[]=`ls -sl`;
    textField -e -text $sel papaObj2;
}

global proc ct_selconD(){
    string $sel[]=`ls -sl`;
    textField -e -text $sel sonObj2;
}
global proc ct_selconE(){
    string $sel[]=`ls -sl`;
    textField -e -text $sel papaObj3;
}

global proc ct_selconF(){
    string $sel[]=`ls -sl`;
    textField -e -text $sel sonObj3;
}
global proc ct_selconG(){
    string $sel[]=`ls -sl`;
    textField -e -text $sel papaObj4;
}

global proc ct_selconH(){
    string $sel[]=`ls -sl`;
    textField -e -text $sel sonObj4;
}

global proc ct_go(){
    string $papaObj1=`textField -q -text papaObj1`;
    string $papaObj2=`textField -q -text papaObj2`;
    string $papaObj3=`textField -q -text papaObj3`;
    string $papaObj4=`textField -q -text papaObj4`;
    
    string $sonObj1=`textField -q -text sonObj1`;
    string $sonObj2=`textField -q -text sonObj2`;
    string $sonObj3=`textField -q -text sonObj3`;
    string $sonObj4=`textField -q -text sonObj4`;
    
    parentConstraint $papaObj1 $sonObj1;
    parentConstraint $papaObj2 $sonObj2;
    parentConstraint $papaObj3 $sonObj3;
    parentConstraint $papaObj4 $sonObj4;
}

proc Gui(){
string $window = `window -title "批量约束工具" -wh 350 120`;
string $col=`columnLayout -adjustableColumn true`;
    rowColumnLayout -numberOfColumns 5 -columnWidth 1 50 -columnWidth 2 100 -columnWidth 3 50 -columnWidth 4 100 -columnWidth 5 50;
        button -label "papa" -c "ct_selconA()";
        textField papaObj1;
        text -label ">>>";
        textField sonObj1;
        button -label "son" -c"ct_selconB()";
        

        button -label "papa" -c "ct_selconC()";
        textField papaObj2;
        text -label ">>>";
        textField sonObj2;
        button -label "son" -c"ct_selconD()";
        

        button -label "papa" -c "ct_selconE()";
        textField papaObj3;
        text -label ">>>";
        textField sonObj3;
        button -label "son" -c"ct_selconF()";
        

        button -label "papa" -c "ct_selconG()";
        textField papaObj4;
        text -label ">>>";
        textField sonObj4;
        button -label "son" -c"ct_selconH()";
        
        button -label "Go" -c "ct_go()" -p $col;
        
showWindow $window;}

if(`window -exists $window`){
    deleteUI -window $window;
}

Gui()
```