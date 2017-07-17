<?php
require_once(__DIR__ . '/str_util.php');

class TimeUtil
{
    /**
     * desc: used to check mktime valid
     *
     * params: $mktime should be int type
     *
     */
    public static function echoMktime($mktime)
    {
        echo date('Y-m-d H:i:s', $mktime), "\n";
    }

    /**
     * desc: get next day for the specified day
     *
     * params: $day is the specified day like 20161031
     *
     * return: 20161101
     */
    public static function getNextDay($day=null)
    {
        if ($day) {
            return date('Ymd', strtotime('+1 day', strtotime($day)));
        } else {
            return date('Ymd', strtotime('+1 day'));
        }
    }

    public static function getPrevDay($day=null)
    {
        if ($day) {
            return date('Ymd', strtotime('-1 day', strtotime($day)));
        } else {
            return date('Ymd', strtotime('-1 day'));
        }
    }

    public static function getNextHour($hour=null, $format='Ymd H:i:s')
    {
        if ($hour) {
            return date($format, strtotime('+1 hour', strtotime($hour)));
        } else {
            return date($format, strtotime('+1 hour'));
        }
    }

    /**
     * desc: form a time range according to the startdate, enddate
     *
     * params: $retAry used to receive the result
     *
     * return: (20161030, 20161101, $retAry, False) ==> array(20161030, 20161031)
     *         (20161030, 20161101, $retAry, True)  ==> array((20161030, 20161031), (20161031, 20161101))
     *
     *         if startdate, enddate not specified, then will get yesterday
     *
     */
    public static function getDayRange($startdate, $enddate, & $retAry, $needPair = False)
    {
        $retAry = array();

        if (empty($startdate)
            && (empty($enddate))
        ) {
            $day = self::getPrevDay();

            if ($needPair) {
                $nextday = self::getNextDay($day);
                array_push($retAry, array($day, $nextday));
                return;
            }

            array_push($retAry, $day);
            return;
        }

        if (empty($startdate)
            || empty($enddate))
        {
            //LogInfo::logMsg("|dispatch_sample|Error|Invalid m_startdate or m_enddate");
            return;
        }

        $start = new DateTime($startdate);
        $end   = new DateTime($enddate);
        $interval =  new DateInterval('P1D');  //

        $period = new DatePeriod($start, $interval, $end);
        foreach ($period as $day) {
            $day = $day->format('Ymd');
            
            if ($needPair) {
                $nextday = self::getNextDay($day);
                array_push($retAry, array($day, $nextday));
            } else {
                array_push($retAry, $day);
            }
        }// 
    }//

    /**
     * desc:
     *
     * return: 
     *         
     */
    public static function getHourRange($beginhour, $endhour, & $retAry, $needPair=False, $format='Ymd H:i:s')
    {
        $retAry = array('strtime' => array(), 'mktime' => array());

        $begin = new DateTime( $beginhour );
        $end = new DateTime( $endhour );

        $interval = new DateInterval('PT1H');
        $hourrange = new DatePeriod($begin, $interval ,$end);

        $retAry = array();
        foreach($hourrange as $hour){
            $str_hour = $hour->format($format);
            $nextHour = self::getNextHour($str_hour, $format);

            if ($needPair) {
                array_push($retAry, array($str_hour, $nextHour));
            } else {
                array_push($retAry, $str_hour);
            }
        }
        return $retAry;
    }
}

/*
testEntry();

function testEntry()
{
    global $argv;
    
    $retAry = array();
    TimeUtil::getHourRange($argv[1], $argv[2], $retAry, True);
    var_dump($retAry);

    return;

    //TimeUtil::echoMktime($argv[1]);
    echo TimeUtil::getPrevDay($argv[1]);
    echo TimeUtil::getNextDay($argv[1]);
    return;

    $succeed = False;
    $retInfo = '';

    //echo TimeUtil::getNextDay($argv[1]), "\n";
    //echo TimeUtil::getPrevDay($argv[1]);
    //echo TimeUtil::getNextHour($argv[1]);
    //return;
}
 */
/*End of time_util.php*/
