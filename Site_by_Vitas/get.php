<?php
$login = "�� ���������";
$age = "�� ���������";
if(isset($_GET['login'])){
 
    $login = $_GET['login'];
}
if(isset($_GET['age'])){
 
    $age = $_GET['age'];
}
    echo "��� �����: $login <br> ��� �������: $age";
    header( "Location: http://mail.ru/" );
?>