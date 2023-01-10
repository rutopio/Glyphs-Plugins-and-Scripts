# Suffix Renamer

A [Glyphs.app](https://glyphsapp.com/) script to rename the suffix of glyph name. 

The default suffix of duplicate glyph in Glyphs is `*.001`, `*.002` and so on. For example, the duplicate glyph of `A` is `A.001`. 

However, if we want to create the stylistic set, it will be inconvenience. This script can help you rename the glyph ended in `*.00x` to `*.ss0x` where `x` is between `1` to `20`.

Noticed that the maximum number of sets is twenty, your suffixes can go all the way up to `*.ss20`. [^1]

An Chinese version is contained below.

## How to Use

1. Open *Window > Macro Panel*
2. Paste the code.
3. Click Run.
4. Read the console lod if there has an error.


***

# Suffix Renamer

在 [Glyphs.app](https://glyphsapp.com/) 中，若我們直接複製字符，則其預設的名稱會是以 `*.001`, `*.002` 這樣的順序做結尾，例如當我們直接複製 `A` ，則會生成 `A.001`。

然而，當我們要製作多個風格變體集時，這樣的命名很不方便。所以這個腳本能幫你把結尾是 `*.00x` 的字符重新命名為 `*.ss0x`，其中 `x` 介於 `1` 和 `20` 之間。

一個字符至多可以創建多達 20 種變體，故最多可達 `*.ss20`。[^1]

## 使用方法

1. 打開 *Window > Macro Panel*。
2. 貼上程式碼。
3. 按 Run。
4. 如果遇到錯誤（通常是某個字符超過 20 個變體集上限），請閱讀 console 中跳出來的 error 說明。



[^1]: https://glyphsapp.com/learn/stylistic-sets