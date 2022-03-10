# GWU CSCI 2541W AWS EC2 Configuration Script
# Created by Ethan Baron, BS CS 2022
​
function usage {
    echo -e "\n\tUSAGE:"
    echo -e "\t\tsudo ./ec2_setup.sh [-h] [-b <BIND ADDRESS>] [-u <MYSQL USERNAME>] [-p <MYSQL PASSWORD>]\n"
    echo -e "\n\tNOTE:"
    echo -e "\t\tWhen you run this script, you'll be expected to enter a number of arguments as \"flags\"."
    echo -e "\t\tIf you don't enter the required arguments, the script will either error out or use an assumed default for each missing argument.\n\n"
    echo -e "\tARGUMENTS:"
    echo -e "\t\t-b <address> : bind address for MySQL. Use the PRIVATE IPV4 ADDRESS of your EC2 instance or 0.0.0.0. If not provided, defaults to \"0.0.0.0\""
    echo -e "\t\t-u <username> : MySQL username. If not provided, defaults to \"ubuntu\""
    echo -e "\t\t-p <password> : MySQL password. If not provided, defaults to \"seas\""
    echo -e "\t\t-h : Show this usage page\n"
    exit 1
}
​
while getopts "hb:u:p:" opt; do
    case $opt in
        h)
            usage;;
        b) 
            if [[ $OPTARG =~ ^[0-9]+.[0-9]+.[0-9]+.[0-9]+$ ]]
            then
                bind_addr=$OPTARG
            else
                echo -e "\n\tError: Bind address syntax. Ensure you are using the PRIVATE IPV4 ADDRESS or 0.0.0.0.\n"
                usage
            fi;;
        u) mysql_username=$OPTARG;;
        p) mysql_password=$OPTARG;;
        \?) usage;;
    esac
done
​
if [ -z "$bind_addr" ]
then
    bind_addr="0.0.0.0"
fi
if [ -z "$mysql_username" ]
then
    mysql_username="ubuntu"
fi
if [ -z "$mysql_password" ]
then
    mysql_password="seas"
fi
​
echo "=================================================================================================================================================="
echo -e "\tGWU CSCI 2541W AWS EC2 Configuration Script"
echo -e "\tCreated by Ethan Baron, GWU BS CS 2022"
echo "=================================================================================================================================================="
​
echo -e "\tINSTALL UTILITIES"
echo -e "\tUpdating apt...\n"
sudo apt-get update
echo -e "\tdone."
echo -e "\tInstalling mysql-server, python3, python3-venv, tmux, python3-pip...\n"
sudo apt-get install -y mysql-server python3 python3-venv tmux python3-pip
echo -e "\tdone."
echo -e "\tChecking program installation...\n"
if [[ -z $(command -v mysql) ]]
then
    echo -e "\tError: MySQL was not installed properly. Please try again."
    exit 1
fi
if [ $(python3 -V | grep -q -e '3.[0-9].[0-9]') ]
then
    echo -e "\tError: Python3 was not installed properly. Please try again."
    exit 1
fi
echo -e "\tdone."
​
echo -e "\n\tCONFIGURING DATABASE"
echo -e "\tEditing MySQL configuration file...\n"
sudo sed -i -r "s/bind-address\t\t= [0-9]+.[0-9]+.[0-9]+.[0-9]+/bind-address\t\t= $bind_addr/" /etc/mysql/mysql.conf.d/mysqld.cnf
echo -e "\tdone."
echo -e "\tRestarting MySQL Service...\n"
sudo service mysql restart
echo -e "\tdone."
echo -e "\tChecking MySQL Service Status...\n"
if ! systemctl is-active --quiet mysql
then
    echo -e "\tError: MySQL is not active."
    exit 1
fi
echo -e "\tdone."
echo -e "\tCreating database user...\n"
sudo mysql --execute="GRANT ALL PRIVILEGES ON *.* TO \"$mysql_username\"@'%' IDENTIFIED BY \"$mysql_password\";"
echo -e "\tdone."
echo -e "\tEnsuring we can login as $mysql_username...\n"
if ! mysql -u $mysql_username -p$mysql_password -e ";" > /dev/null 2> /dev/null
then
    echo -e "\tError: Could not login to MySQL."
    exit 1
fi
echo -e "\tdone."
​
echo -e "\n\tSETTING UP FLASK"
echo -e "\tEnsuring pip is installed..."
sudo apt-get install python3-pip
echo -e "\tdone."
echo -e "\tInstalling modules with pip..."
python3 -m pip install -U flask mysql-connector
echo -e "\tdone."
​
echo -e "\n"
echo "=================================================================================================================================================="
echo -e "\tINSTALLATION COMPLETE. SUMMARY:"
echo -e "\tEC2 Setup Completed Successfully. Please ensure you test flask and can connect to your instance in a web browser."
echo -e "\tInstalled python3, mysql-server, tmux, pip."
echo -e "\tVerified versions for Python3, MySQL."
echo -e "\tMySQL Bind Address set to $bind_addr."
echo -e "\tMySQL User created with username $mysql_username and password $mysql_password."
echo -e "\tNOTE: If MySQL user existed already, password has been overwritten."
echo -e "\tFlask and mysql-connector installed successfully."
echo "=================================================================================================================================================="