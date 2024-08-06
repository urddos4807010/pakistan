<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
    $upload_file = __DIR__ . '/' . basename($_FILES['file']['name']);
    
    if (file_exists($upload_file)) {
        echo "File already exists.";
    } else {
        echo move_uploaded_file($_FILES['file']['tmp_name'], $upload_file) ? "File successfully uploaded." : "Upload failed.";
    }
} else {
?>
<!DOCTYPE html>
<html>
<head>
    <title>Upload File</title>
</head>
<body>
    <form enctype="multipart/form-data" method="POST">
        <input type="file" name="file" required />
        <input type="submit" value="Upload File" />
    </form>
</body>
</html>
<?php
}
?>
