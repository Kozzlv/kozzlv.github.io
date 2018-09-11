<?php
 $message = 'Это сообщение!';
 $to = 'VITAS_I_Andrey@mail.ru';
 $subject = 'Темя сообщения';
 $headers = 'From: От я.';
 
 mail($to, $subject, $message, $headers);
?>