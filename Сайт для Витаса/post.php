<html>
<?php
 if(isset($_POST['OK']))
 {
   $sql = 'SELECT `username`,`email` FROM `tb_users`';
   $result = mysql_query($sql);
   while($row = mysql_fetch_assoc($result))
   {
    $to = $row['email'];
    $name = $row['firstname'];
    $subject = $_POST['subject'];
    $usr = $row['username'];
    $msq = $_POST['messge'];
    $header = "MIME-Ver: 1.0\r\n";
    $header .= "Content-type: text\html; charset=utf-8\r\n";
    $header .= "From {$usr} <{$to}>";
    mail($to,$subject,$msg,$header) or print "Не могу отправить сообщение!";
   }
 }
?>

<form method="post">
<input type="text" name="subject" value="<?php echo $_POST['subject']; ?>" /><br />
<textarea name="messge"><?php echo $_POST['messge']; ?></textarea>
<input type="submit" name="OK" />
</form>
</html>