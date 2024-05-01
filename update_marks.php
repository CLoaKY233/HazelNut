<?php

$servername = "localhost";
$username = "root";
$password = "1234";
$dbname = "project_exhibition";
$conn = mysqli_connect($servername, $username, $password,$dbname);

// Die if connection was not successful
if (!$conn){
    die("Sorry we failed to connect: ". mysqli_connect_error());
}

if ($_SERVER['REQUEST_METHOD'] == 'POST'){
$reg_number = $_POST["reg_number"];
$review = $_POST["review"];
$marks = $_POST["marks"];
    

// **Security Warning:** This is a basic example and doesn't use prepared statements to prevent SQL injection.
$sql = "UPDATE student_marks SET ".$review." = ".$marks." WHERE REGISTER_NO = '".$reg_number."'";

$result = mysqli_query($conn, $sql);


if($result){
    if (mysqli_affected_rows($conn) > 0) {
    echo '<div class="alert alert-success alert-dismissible fade show" role="alert">
    <strong>Success!</strong> Marks for ' . $reg_number.' have been updated successfully!
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
      <span aria-hidden="true">×</span>
    </button>
  </div>';
} else {
    echo '<div class="alert alert-danger alert-dismissible fade show" role="alert">
    <strong>Error!</strong> Registration number ' . $reg_number.' not found or no changes were made.
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
      <span aria-hidden="true">×</span>
    </button>
  </div>';
}}
else{
    echo "We could not update the record successfully";
}

$conn->close();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <link rel="stylesheet" href="styles.css">

    <title>Update Student Marks</title>
</head>
<body>
<div class="container">
    <h1>Update Student Marks</h1>
    <form action="/projectExhibition/update_marks.php" method="post">
        <label for="reg_number">Registration Number:</label>
        <input type="text" name="reg_number" id="reg_number" required><br><br>

        <label for="review">Update Review:</label>
        <select name="review" id="review">
            <option value="Review_1">Review 1</option>
            <option value="Review_2">Review 2</option>
            <option value="Review_3">Review 3</option>
        </select><br><br>
        <!-- <label for="review">Update Review:</label>
        
        <input type="number" name="review" id="review" min="0" max="3" required><br><br> -->
        
        
        <label for="marks">New Marks:</label>
        <input type="number" name="marks" id="marks" min="0" max="100" required><br><br>
        <button type="submit">Update Marks</button>
    </form>
</div>

<script>
        // Close alert message when close button is clicked
        document.querySelectorAll('.alert .close').forEach(function(closeBtn) {
            closeBtn.addEventListener('click', function() {
                this.parentElement.classList.remove('show');
            });
        });
    </script>
</body>
</html>