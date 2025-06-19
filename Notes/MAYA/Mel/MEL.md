- 删除物体的混合变形：
```
string $objsel[]=`ls -sl`;

string $object1[]=`listConnections -s true ($objsel[0]+".inMesh")`; 

delete($object1);
```
- 显示选中骨骼数量

```
size(`ls -sl -type "joint"`);
```