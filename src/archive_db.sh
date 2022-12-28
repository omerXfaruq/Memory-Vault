while true
do
	curl -v -F "chat_id=-1001786782026" -F document=@database.db https://api.telegram.org/bot${1}/sendDocument
	sleep ${2}
done