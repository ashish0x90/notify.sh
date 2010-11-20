# echo "test begin"
# ./check.sh $? "notification.cfg"
# echo "hello - OK"
# ./check.sh $? "notification.cfg"
# asdef;
# ./check.sh $? "notification.cfg"
# echo "test_done - OK"
# echo "end - OK"

mkdir test
./check.sh $? "notification.cfg"
mkdir test
./check.sh $? "notification.cfg"
rm -r test
./check.sh $? "notification.cfg"