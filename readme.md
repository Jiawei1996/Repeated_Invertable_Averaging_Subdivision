## 概述

该项目旨在设计一种基于Lane-Riesenfeld细分中重复平均思想的、具有逆向细分规则的细分模式，并基于所设计的细分法设计相应的多分辨率表示模式，涉及曲线和曲面。

## 意义

Lane-Riesenfeld算法是一种只需"一次加细+n次平滑"便可生成n阶光滑极限曲线的细分法，该算法不仅思想简单，而且具有较强的推广性。只要目标空间中具有两点线性插值方法，便可以将Lane-Riesenfeld算法中的线性平均替换为目标空间中的平均，并实现目标空间中的曲线细分。典型的，有球面上的球面线性插值平均，便可使用所述方法得到球面上的细分法。

得到一种可逆细分法后便可以基于该细分构造目标空间中的多分辨率表示了，这在实际应用中具有一定的实用价值，见两个demo文件夹。

## 注意

- 该项目只整理了三重曲线细分的代码，包括欧氏空间和球面空间。关于二重细分的算法可以参考[这篇文献](https://www.researchgate.net/publication/303465157_Multiresolution_on_Spherical_Curves)。

- 曲面多分辨率中的分解调整参考了[这篇文献](https://www.researchgate.net/publication/220250625_Multiresolution_for_curves_and_surfaces_based_on_constraining_wavelets)中的思想。