# Wrong Overlapping Path Detector

![](demo.png)

A [Glyphs.app](https://glyphsapp.com/) script to find the wrong direction whenever two shapes have intersections. 

It is commonly found when we use `Reconnect Nodes` to split one shape into two. The glyph will have blank intersections if the condition is unresolved.

A Chinese version is contained below.

## How to Use

1. Open *Window > Macro Panel*
2. Paste the code.
3. Click Run.
4. Read the console log.

***

# Wrong Overlapping Path Detector

在 [Glyphs.app](https://glyphsapp.com/) 中，當我們透過 `Reconnect Nodes` 將一個路徑拆分成兩個的時候，有時候會出現路徑方向錯誤，致使字符在渲染後，出現空白交錯區的情況。

本腳本可以協助您挑出那些有問題的字符。

## 使用方法

1. 打開 *Window > Macro Panel*。
2. 貼上程式碼。
3. 按 Run。
4. 若發現有問題的字，在 console 中會顯示有問題的字符名稱。