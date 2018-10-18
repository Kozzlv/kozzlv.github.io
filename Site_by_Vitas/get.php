<?php
$login = "не определен";
$age = "не определен";
if(isset($_GET['login'])){
 
    $login = $_GET['login'];
}
if(isset($_GET['age'])){
 
    $age = $_GET['age'];
}
    echo "Ваш логин: $login <br> Ваш возраст: $age";
    header( "Location: http://mail.ru/" );
?>