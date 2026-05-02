### ENGLISH

## Multiplayer Pong on LAN

A simple LAN-based multiplayer Pong game made to demonstrate basic 
Computer Network interactions like sending data between devices and syncing 
states developed using Python.


## Features
- Host & Client architecture (TCP socket-based)
- Supports up to 4 players: 1 Host and 3 Clients
- Gamestate synchronization between all users
- Lobby system before game start
- Error Handling when a player disconnects


## How the game works:
- The Host acts as the game server
- Clients connect to the host via IP address over a TCP connection
- The host update ball movement, paddles, lives etc (gamestate) and sends 
the gamestate data to clients
- The clients send data to the Host and receive gamestate from Host
- Paddles are controlled with WASD or arrow keys

## Libraries used
-socket library used to make TCP connections and send data to Clients across local network
-Pygame and random libraries used to implement a simple Pong game
-json library for wrapping gamestate data to encode via socket library
-os and sys libraries used to find .py file locations
-subprocess library to open .py files

## Dependencies
-The game runs on Python 3.13.13 on Windows and requires Pygame and Socket libraries to function.
Both can be installed using Pip, although you might need an earlier version of Python to 
install Pygame via Pip.

## Possible problems with connection
-Your or Client's Computers' firewalls or your WiFi's Firewalls can block python from making connections
and sending data across the local network. To fix this you can whitelist python on your firewalls and try again


### TÜRKÇE 

## Çok Oyunculu LAN Pong 

Bu proje, Python kullanılarak geliştirilmiş, cihazlar arasında veri gönderme ve 
durum senkronizasyonu gibi temel Bilgisayar Ağları kavramlarını göstermek amacıyla
 yapılmış basit bir LAN tabanlı çok oyunculu Pong oyunudur.

## Özellikler
-Host & Client mimarisi (TCP bağlantılı)
-4 oyuncuya kadar destek: 1 Host ve 3 Client
-Tüm oyuncular arasında oyun bilgileri (gamestate) senkronizasyonu
-Oyun başlamadan önce lobi sistemi
-Oyuncu bağlantısı kesildiğinde hata yönetimi

## Oyun Nasıl Çalışır:
-Host, oyun sunucusu olarak görev yapar
-Client’lar, IP adresi üzerinden TCP bağlantısı ile host’a bağlanır
-Host; top hareketi, raketler, canlar vb. oyun durumunu günceller ve client’lara gönderir
-Client’lar host’a veri gönderir ve host’tan oyun durumunu alır
-Raketler WASD veya yön tuşları ile kontrol edilir


## Kullanılan Kütüphaneler
-socket : TCP bağlantısı kurmak ve yerel ağ üzerinden veri göndermek için kullanıldı
-pygame ve random: Basit bir Pong oyunu geliştirmek için kullanıldı
-json: gamestate verisini bir String olarak kodlayıp soket üzerinden göndermek için kullanıldı
-os ve sys: .py dosyalarının konumlarını bulmak için kullanıldı
-subprocess: .py dosyalarını çalıştırmak için kullanıldıi

## Gereksinimler
-Oyun, Windows üzerinde Python 3.13.13 ile çalışır ve Pygame ile Socket kütüphanelerini gerektirir
-Her iki kütüphane de Pip ile kurulabilir, ancak Pygame’i kurabilmek için daha eski bir Python sürümüne ihtiyaç duyabilirsiniz

## Olası Bağlantı Problemleri
-Sizin veya client’ın bilgisayarındaki güvenlik duvarı ya da Wi-Fi ağınızın güvenlik duvarı, Python’un bağlantı kurmasını engelleyebilir
Bunu çözmek için Python’u güvenlik duvarında beyaz listeye ekleyip tekrar deneyebilirsiniz