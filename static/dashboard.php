<?php
session_start();
require 'lang.php';

// Check if the user is logged in
if (isset($_SESSION['username'])) {
    $username = $_SESSION['username'];
    //$conn=$_SESSION['db_conn'];
} else {
    // Redirect to the login page if the user is not logged in
    header("Location: login.php");
    exit();
}
$conn = pg_connect("host=localhost port=5432 dbname=vms user=postgres password=0000");
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="dashboard.css">
    <script src="menu.js"></script>
    <title>VAAHAN - Dashboard</title>
</head>

<body>
    <nav class="navbar">
        <div class="container">
            <div class="navbar-left">
                <h1 class="logo"><b>&nbsp;&nbsp;&nbsp;&nbsp;<?=__('VAAHAN')?></b></h1>
            </div>
            <div class="back-button">
                <a href="#" onclick="history.go(-1);">
                  <img src="backbutton.png" alt="Back">
                </a>
            </div>
            <div class="navbar-right">
                <ul class="nav-links">
                    <li><a href="AboutUs.php"><?=__('About us')?></a></li>
                    <li><a href="#"><?=__('Profile')?></a></li>
                    <li><a href="Servicing.php"><?=__('Servicing')?></a></li>
                    <li><div class="dropdown">
                        <a onclick="myFunction()" class="dropbtn"><?=__('Language')?></button>
                        <div id="myDropdown" class="dropdown-content">
                            <div><a href="dashboard.php?lang=en">&nbsp;&nbsp;&nbsp;&nbsp;English</a></div>
                            <div><a href="dashboard.php?lang=hn">&nbsp;&nbsp;&nbsp;&nbsp;हिंदी</a></div>
                            <div><a href="dashboard.php?lang=mr">&nbsp;&nbsp;&nbsp;&nbsp;मराठी</a></div>
                        </div>
                    </div></li>
                    <li><a href="login.php"><?=__('Logout')?></a></li>
                </ul>
            </div>
        </div>
    </nav>

    <header class="dashboard-header">
        <h1><?=__('Welcome')?>, <?php echo $username; ?></h1>
        <p><?=__('Manage your vehicle documents with ease.')?></p>
    </header>

    <section class="vehicle-details">
        
        <div class="details-container">
            <div class="details-card">
                <h3><?=__('Vehicle Information')?></h3>
<?php
if (isset($_SESSION['username'])){
    $query2 = "SELECT vehicle_no, registration_no, maker_name, vehicle_type, vehicle_name, model_name, fuel_type, PUCC_no, PUCC_validity FROM vehicle_details WHERE user_id='$_SESSION[user_id]';";
    $request = pg_query($conn, $query2);
    if($request){
        while($row = pg_fetch_assoc($request)){
            echo"<ul>
            <li>Vehicle no.: ".$row["vehicle_no"]."</li>
            <li>Registration no.: ".$row["registration_no"]."</li>
            <li>Maker name: ".$row["maker_name"]."</li>
            <li>Vehicle type: ".$row["vehicle_type"]."</li>
            <li>Vehicle name: ".$row["vehicle_name"]."</li>
            <li>Model name: ".$row["model_name"]."</li>
            <li>Fuel type: ".$row["fuel_type"]."</li>";
              // Check if PUCC_no and PUCC_validity are set before accessing them
              if (isset($row["PUCC_no"])) {
                echo "<li>PUCC no.: " . $row["PUCC_no"] . "</li>";
            }
            if (isset($row["PUCC_validity"])) {
                echo "<li>PUCC validity: " . $row["PUCC_validity"] . "</li></ul>";
            }
        }
    }
}
?>
            </div>

            <!-- <div class="details-card">
                <h3><?=__('Insurance Details')?></h3>
                <ul>
                    <li><span>Insurance Company:</span> XYZ Insurance</li>
                    <li><span>Policy Number:</span> XYZ123</li>
                    <li><span>Expiry Date:</span> 2023-06-30</li>
                </ul>
            </div>
        </div> -->
    </section>

    <section class="dashboard-overview">
        <div class="overview-card">
            <h2><?=__('Documents Uploaded')?></h2>
            <p class="count">4</p>
        </div>

        <div class="overview-card">
            <h2><?=__('Renewal Reminders')?></h2>
            <p class="count">3</p>
        </div>

        <!-- <div class="overview-card">
            <h2>Accessibility Anytime, Anywhere</h2>
            <p class="count"><?=__('Yes')?></p>
        </div> -->
    </section>

    <section class="dashboard-features">
        <h2><?=__('Key Features')?></h2>
        <ul>
            <li><?=__('Effortless document uploads and management.')?></li>
            <li><?=__('Automated renewal reminders for essential documents.')?></li>
            <li><?=__('Secure and accessible anytime, anywhere.')?></li>
            <li><?=__('Smart search for quick document retrieval.')?></li>
        </ul>
    </section>

    <section class="dashboard-recent-docs">
        <h2><?=__('Recently Uploaded Documents')?></h2>
        <ul>
            <li><?=__('Document 1 - Insurance Certificate')?></li>
            <li><?=__('Document 2 - Vehicle Registration')?></li>
            <li><?=__('Document 3 - Driver License')?></li>
            <li><?=__('Document 4 - PUCC')?></li>
        </ul>
    </section>

    <footer class="dashboard-footer">
        <p>&copy; 2024 VAHAAN. All rights reserved.</p>
    </footer>
</body>

</html>
