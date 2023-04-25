<?php
$script_path = " /var/www/html/symphonyGPT.py";
// Command to run the Python script
try {
$command = "/usr/bin/python3 " . " " . $script_path . " \"" . $_GET['question'] . "\"" . " 2>&1";

// Call the Python script using exec()
echo $command;
$result = shell_exec($command);
} catch(Exception $e) {
    echo " errorrrrrrr";
}
// Print the result
header("Content-Type: application/json");
// $result = [
//     'query' => 'select * from table1;',
//     'result-table' => 'col0\n123',
//     'answer' => 'Hiiii',

// ];
$result = json_encode($result);
echo $result;
?>
