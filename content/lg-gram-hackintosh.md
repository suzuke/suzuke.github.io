Title: LG Gram 黑蘋果全記錄	
Date: 2020-05-24 00:48	
Modified: 2020-05-24 00:48	
Category: Hackintosh	
Tags: lg-gram, hackintosh, 黑蘋果	
Slug: lg-gram-hackintosh	
Authors: suzuke	
Summary: 記錄在LG-Gram 筆電上安裝黑蘋果的歷程

#Step0. 前言
前陣子因為工作上需要使用到 IOS 的開發環境，而 IOS 綁定了 Mac OS 底下的 Xcode ，但是因為我手上的設備是 2012 年的 Macmini，那速度可真的不是一般人能忍的。 但是新款 Macmini 的價格又令人卻步，在考慮到性價比還有自己愛折騰的心之下，開始有了黑蘋果的想法。

#Step1. 認識黑蘋果(Hackintosh)
黑蘋果 (Hackintosh) 的意思即是在在非蘋果授權的 x86 架構電腦上安裝 Ｍac OS ， Hackintosh 一詞也是衍生自蘋果官方的電腦系統名稱 Macintosh。	
早先，蘋果電腦使的 CPU 架構都是 IBM 所生產的 PowerPC 處理器，直到 2005 年開始，才轉由與 Intel 合作使用 x86-64架構的處理器，從這個時候開始才大幅降低了黑蘋果的門檻，讓一般不需要具備太深入技術的人也可以進入黑蘋果的世界。	
##EFI Bootloader
##DSDT/SSDT
#Step2. 安裝前準備
## BIOS 設定
## 製作安裝隨身碟 
#Step3. 安裝完成後修正
## 觸控板驅動 (VoodooI2C)
觸控板驅動向來都是黑蘋果中最難解決的問題，筆記型電腦的觸控板在黑蘋果中的支援度都不太高。幸運的是，目前 I2C 觸控板主流都是使用 [VoodooI2C](https://github.com/VoodooI2C/VoodooI2C) ，而 LG-Gram z980 的 I2C 觸控板 (pci8086,9d60) 是被完美支援 (GPIO interrupts) 的。

不過雖然說是完美支援，我們仍然需要使用 SSDT Patch 來確保 GPIO 是正確的被啟用。另外根據 LG-Gram 的 [ACPI 定義](https://raw.githubusercontent.com/suzuke/LG-Gram-13z980-Opencore/master/ACPI_Origin/DSDT.dsl) ，觸控板 (TPD0) 會隨著當前的作業系統(\_OSI)而有不同的啟用狀態：

```
Method (_STA, 0, NotSerialized)  // _STA: Status
{
    If (LEqual (PTPS, One))
    {
        Return (0x0F)
    }

    If (LOr (LEqual (SDS0, 0x05), LOr (LEqual (SDS0, One), LOr (LEqual (SDS0, 0x02), LEqual (SDS0, 0x06)))))
    {
         Return (0x0F)
    }

    Return (Zero)
 }
```
我選擇的做法是直接將原本的 TPD0 禁用，再使用 [SSDT-TPXX](https://github.com/suzuke/LG-Gram-13z980-Opencore/blob/master/ACPI_Patch/SSDT-TPXX.dsl) 來建立出新的 TPDX 裝置。
禁用設備的方式可以參考 [OC-little I2C專用部件](https://github.com/daliansky/OC-little/tree/master/20-I2C%E4%B8%93%E7%94%A8%E9%83%A8%E4%BB%B6)。

## FN Key 功能修正
筆記型電腦的 FN Key 功能通常都伴隨著 EC（Embed Controller，嵌入式控制器）的 Query 事件，也就是說每當我們按了某個 FN + Fx 的組合鍵時，同時在 ACPI 中也會有相對應的函數 (_Qxx) 被呼叫。所以我們只要找出每一個 FN組合鍵對應的 Query 函數，就可以實作出應有的功能。

以下這邊就是透過 [ACPIDebug](https://github.com/daliansky/OC-little/tree/master/18-ACPIDebug) 在 Query 函數中印出 log 找出的：

| FN Key | EC Query | 對應功能 | 備註 |
|  :----: | :----:  | :----: | :----: |
| FN + F1 | _QFF | Null |
| FN + F2 | _Q40 | 減低亮度 |
| FN + F3 | _Q40 | 增加亮度 |
| FN + F4 | _Q34 | 睡眠 |
| FN + F5 | _QFF | 觸控板開關 |
| FN + F6 | _Q36 | 飛航開關 | 
| FN + F7 | _Q37 | 多螢幕連結 |
| FN + F8 | _Q30 | 鍵盤燈開關 |
| FN + F9 | _Q40 | 螢幕暖色 | 
| FN + F10 | Null | 音量靜音 | 
| FN + F11 | Null | 減低音量 | 
| FN + F12 | Null | 增加音量 |
| FN + PrtSc | Null | Null |  

根據上面的資料所做的 SSDT Patch 在這 [SSDT-FNKey](https://github.com/suzuke/LG-Gram-13z980-Opencore/blob/master/ACPI_Patch/SSDT-FNKey.dsl) (only for LG-Gram) 。

需要注意的是，根據 ACPI 中 _OSI 的參數不同，同一個 FN 組合鍵所對應的 Query 函數也有可能不一樣，上面所得到的資料，並 **沒有** 使用 [_OSI to XOSI](https://github.com/daliansky/OC-little/tree/master/04-%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F%E8%A1%A5%E4%B8%81) 更名，所以如果你想直接使用我提供的SSDT-FNKey Patch，那你也不應該使用 \_OSI to XOSI 更名。

## 電池電量顯示修正

#Step4. 參考
[EC、BIOS、vBIOS是什麼?](https://www.cjscope.com.tw/cht/faq_detail.php?serial=45)
[OC-little](https://github.com/daliansky/OC-little)
