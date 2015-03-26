<?
#########################################################################
#                                                                       #
# Name:       PQPRO PHP                                                 #
#                                                                       #
# Started:    2011010800                                                #
# Decription: Library that enable PHP to send queries to PQPro          #
#                                                                       #
# Important: WHEN EDITING THIS FILE, USE SPACES TO INDENT - NOT TABS!   #
#                                                                       #
##########################################################################
#                                                                       #
# Juan Miguel Taboada Godoy <juanmi@centrologic.com>                    #
#                                                                       #
# This file is part of PQPRO.                                           #
#                                                                       #
# PQPRO is free software: you can redistribute it and/or modify         #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 2 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# PQPro is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          #
# GNU General Public License for more details.                          #
# You should have received a copy of the GNU General Public License     #
# along with PQPRO.  If not, see <http://www.gnu.org/licenses/>.        #
#                                                                       #
#########################################################################

/* Send a query to a PQPRO system
 * 
 * Parameters:
 * -`url`:      URL to the remote system as 'http[s]://<host>[:<port>]'
 *              Example: http://protocol.system.dom/pqpro/
 *              Example: https://protocol.system.dom:443
 *
 * -`query`:    String to send to the remote system
 *
 * -`user`:     Username to use for authentication in the remote system
 *
 * -`password`: composed password as "$<algorithm M:md5() S:sha1()>$<encryption_key>"
 *              Example: $M$df83djfdfhdfhdfidfjdfh3u3jfdf
 */
function pqpro($url,$query,$user,$password) {
    
    // Split the password
    $password_splitted = split('\$',$password);
    if (count($password_splitted)!=3) {
        throw new Exception("The password has wrong format!");
    }
    list($g,$algorithm,$encryption_key) = $password_splitted;
    // Controller
    if (strlen($g)>0) { throw new Exception("Garbage detected in the password!"); }
    if (strlen($encryption_key)<16) { throw new Exception("Encryption key is too short!"); }
    
    // Choose the hashing algorithm
    if ($algorithm=='M') {          $hasher='md5';
    } else if ($algorithm=='S') {   $hasher='sha1';
    } else {                        throw new Exception("Wrong algorithm used inside the password!");
    }
    $hashfunc = create_function('$string', "return $hasher(\$string);");
    
    // Make the signature
    $query_hash=$hashfunc($query);
    $signature=$hashfunc($query_hash.$user.$query_hash.$encryption_key.$query_hash);
    
    // Inicialize CURL session and setup the URL
    $link = curl_init();
    curl_setopt($link, CURLOPT_URL, $url);
    
    // Setup how to check authentication
    curl_setopt($link, CURLOPT_HTTPAUTH, CURLAUTH_ANY);
    
    // Add personalized heaaders
    curl_setopt($link, CURLOPT_HEADER, 1);
    curl_setopt($link, CURLOPT_HTTPHEADER, array('Content-Type: application/json')); 
    curl_setopt($link, CURLOPT_HTTPHEADER, array("Signature: $signature"));  
    
    // Send data using POST, don't verify SSL certificate and return result instead printing it
    curl_setopt($link, CURLOPT_POST, 1);
    curl_setopt($link, CURLOPT_POSTFIELDS, $query);
    curl_setopt($link, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($link, CURLOPT_RETURNTRANSFER, 1);
    
    // Get result
    $data = curl_exec($link);
    
    // Disconnect
    curl_close($link); 
    
    // Split answer in header and body
    $data_exploded = explode("\r\n\r\n", $data, 2);
    if (count($data_exploded)==2) {
        list($headers, $body) = $data_exploded;
    } else {
        $headers = $data_exploded[0];
        $body = '';
    }
    $headers_exploded = explode("\r\n", $headers);
    $signature = NULL;
    foreach ($headers_exploded as $line) {
        if (strstr($line,"Signature: ")) {
            list($head, $signature) = explode("Signature: ", $line);
            break;
        }
    }
    
    // Get the answer
    // $answer=$body_exploded[count($body_exploded)-1];
    $answer=$body;
    
    // Check the signature
    $validation=false;
    if ($signature) {
        $answer_hash = $hashfunc($answer);
        $newsignature = $hashfunc($answer_hash . $user . $answer_hash . $encryption_key . $answer_hash);
        if ($signature == $newsignature) {
            $validation = true;
        } 
    }
    
    // Return if answer has been validated and the answer we got
    return array($validation, $answer);
}

$user='br0th3r';
$password='$M$12340897123408971234089712340897';
$query=array();
$query['config']=array();
$query['config']['user']="br0th3r";
$query['config']['service']="paquetes";
$query['config']['action']="tarificar";
$query['config']['enviroment']="dev";
$query['abc']='def';
$query['ghi']='ijk';

list($validation,$answer)=pqpro("http://www.website.foo/pqpro/",json_encode($query),$user,$password);

echo "ANSWER: ";
var_export($answer);
echo "<br>";
echo "VALIDATION: ";
var_export($validation);

?>
