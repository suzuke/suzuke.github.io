Title: 用Python在Github上寫網誌
Date: 2020-05-12 22:20
Category: Python
Tags: pelican, publishing
Slug: my-super-post
Authors: suzuke
Summary: 

# 前言
其實早在很久之前，就一直聽聞 Github 可以透過靜態頁面的方式來寫網誌。但終沒有認真的找個時間好好的研究，剛好這一次的每週活動是需要練習寫文章，也就藉著這次的機會，順便研究一下到底要怎麼透過 Github 來寫網誌。

## Step1. 安裝 Pelican 和建立 git repository
首先必須先安裝 **Pelican** 和 **ghp-import**，我們可以非常簡單地透過 pip 來安裝。

`$ pip install pelican ghp-import`

Pelican 提供兩種編寫文章的格式，分別是 reStructuredText 跟 Markdown，因為我自己本身對 Markdown比較熟悉，所以這邊我選擇使用 Markdown，一樣透過 pip 來安裝 Markdown。

`$ pip install Markdown`

安裝完所需要的軟體，再來我們需要在 Github 上建立一個空的 git 資料庫(repository)。
不知道怎麼建立 git 資料庫的人，可以參考[這裡](https://help.github.com/en/github/getting-started-with-github/create-a-repo)。
記得這個資料庫的命名一定要是以下這種形式：

`https://github.com/username/username.github.io`

接著我們就把它 clone 下來吧！

```
$ git clone https://GitHub.com/username/username.github.io blog
$ cd blog
```

## Step2. 建立 Content branch
因為我們是使用 Markdown 格式寫完文章，再透過 Pelican 幫我們產生出靜態網頁所需要的資源，
一般來說我們會建議把 Markdown 格式的原始文件另外存放在另一個 branch 裡，這樣在管理上會簡單許多。

```
$ git checkout -b content
Switched to a new branch 'content'
```

## Step3. 設定 Pelican
現在我們要開始對 Pelican 做設定，Pelican	提供了一個快速的設定工具 **pelican-quickstart**，只要依序回答完問題，就完成設定了。

```
$ pelican-quickstart
Welcome to pelican-quickstart v3.7.1.

This script will help you create a new Pelican-based website.

Please answer the following questions so this script can generate the files
needed by Pelican.

> Where do you want to create your new web site? [.]  
> What will be the title of this web site? Super blog
> Who will be the author of this web site? username
> What will be the default language of this web site? [en]
> Do you want to specify a URL prefix? e.g., http://example.com   (Y/n) n
> Do you want to enable article pagination? (Y/n)
> How many articles per page do you want? [10]
> What is your time zone? [Europe/Paris] US/Central
> Do you want to generate a Fabfile/Makefile to automate generation and publishing? (Y/n) y
> Do you want an auto-reload & simpleHTTP script to assist with theme and site development? (Y/n) y
> Do you want to upload your website using FTP? (y/N) n
> Do you want to upload your website using SSH? (y/N) n
> Do you want to upload your website using Dropbox? (y/N) n
> Do you want to upload your website using S3? (y/N) n
> Do you want to upload your website using Rackspace Cloud Files? (y/N) n
> Do you want to upload your website using GitHub Pages? (y/N) y
> Is this your personal page (username.github.io)? (y/N) y
Done. Your new project is available at /Users/username/blog
```
設定完之後，可以看一下現在目前的資料夾內是長這個樣子的。每個檔案的功能可以到  [Pelican文件](https://docs.getpelican.com/en/stable/) 查詢。

```
$ ls
Makefile                content/        develop_server.sh*
fabfile.py              output/         pelicanconf.py
publishconf.py
```

最後再將這些 Pelican 產生出來的檔案，都 commit 和 push 到 content branch上吧，這樣我們就完成了前置的設定囉。

```
$ git add .
$ git commit -m 'initial pelican commit to content'
$ git push origin content
```

## Step4. 編寫你的第一篇文章
恭喜你可以開始建立跟編寫你的第一篇文章囉！ 這邊我們也順便把 **關於我** 的頁面也都一併建立出來吧。

```
$ cd content
$ mkdir pages images
$ cp /Users/username/SecretStash/HotPhotoOfMe.jpg images
$ touch first-post.md
$ touch pages/about.md
```
用文字編輯器打開 first-post.md 來編寫你的文章，格式如下，[詳細見這](https://docs.getpelican.com/en/stable/content.html#file-metadata)：

```
Title: 我的第一篇文章
Date: 2020-05-12 20:20
Modified: 2020-05-12 23:30
Category: Python
Tags: pelican, publishing
Slug: my-super-post
Authors: Suzuke
Summary: 我是摘要

文章的內容在這裡唷！
```

編輯 **關於我** 的頁面，打開 pages/about.md

```
title: 關於我
date: 2020-05-12

![handsomeguy]({static}/images/HotPhotoOfMe.jpg)

```
使用 Pelican 產生靜態網頁到 output 資料夾：

`$ pelican content -o output -s publishconf.py`

使用 ghp-import 把 output 的內容都 commit 到 master branch 上：

`$ ghp-import -m "Generate Pelican site" --no-jekyll -b master output`

把本地端的 master 推送到遠端 github 上：

`$ git push origin master`

最後把本地端 content 裡的 Markdown 原始文件都 commit & push 到遠端 github 上：

```
$ git add content
$ git commit -m 'added a first post, a photo and an about page
$ git push origin content
```

## Step5. 