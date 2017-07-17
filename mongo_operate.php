<?php
require_once(dirname(__FILE__) . '/../conf/project_conf.php');
require_once(__DIR__ . '/log_info.php');

define ('MAX_LIMIT_COUNT', 100000);

class MongoOperate {
    /**
     * desc: insert document into collection according to collection name
     *
     * params: $keyname  like 'url_hits', 'url_dl', etc
     *              more info see about ./project_conf.php
     *
     *         $doc , $option  see MongoCollection::insert
     *
     *         & $insertedId used to receive the mongod id
     *         & $succeed    used to receive operation status, succeed (True) or fail (False)
     *         & $errInfo    used to receive error info if exists, otherwise null
     *
     *
     *
     * return:  if succeed, $succeed will be set True, $insertedId will be set, $errInfo will be '';
     *          if failed,  $succeed will be set False, $insertedId will be null, $errInfo will be set
     *
     **/
    public static function insertData($keyname, 
                                      $doc, $option, 
                                      & $insertedId, 
                                      & $succeed,
                                      & $errInfo,
                                      $mongodb = null)
    {
        $succeed = False;
        $errInfo = '';
        $insertedId = null;

        $collection = self::getCollection($keyname, $errInfo, $mongodb);
        if (!$collection) {
            return;
        }

        try {
            $collection->insert($doc, $option);
        } catch (MongoException $e) {
            $errInfo = sprintf("|MongoOperate|Exception|insertData %s %s,%s", 
                                $keyname, $e->getCode(), $e->getMessage());
            return;
        }

        $insertedId = $doc['_id'];

        $succeed = True;
        $errInfo = '';
        return;
    }

    /**
     * desc: batch insert, see MongoBatchInsert
     *
     * params: $keyname like url_hits, url_dl, etc, 
     *           more info to see project_conf
     *
     *         $docs  array of $doc to be inserted
     *         
     *         & $succeed used to receive operate status
     *         & $errInfo used to receive error info
     * return:
     *
     **/
    public static function batchInsertData($keyname, 
                                          & $docs,
                                          & $succeed,
                                          & $errInfo,
                                          $constructOption = array(),
                                          $execOption = array(),
                                          $mongodb = null)
    {
        $succeed = False;
        $errInfo = '';

        $collection = self::getCollection($keyname, $errInfo, $mongodb);
        if (!$collection) {
            return;
        }

        try {
            $batch = new MongoInsertBatch($collection, $constructOption);
            foreach ($docs as $doc) {
                $batch->add($doc);
            }

            $batch->execute($execOption);

        } catch (MongoException $e) {
            $errInfo = sprintf("|MongoOperate|Exception|batchInsert %s %s,%s", 
                                $keyname, $e->getCode(), $e->getMessage());
            return;
        }

        $succeed = True;
        return;
    }

    /**
     * desc: update 
     *
     * params: keyname used for collection, like 'new_url_hits', 'path2_related_hosts',
     *                  see ./project_conf.php
     *         criteria, etc see MongoCollection::updateData
     *         
     *         & $succeed used to receive operation status
     *         & $errInfo used to receive error info
     *         
     * return:
     **/
    public static function updateData($keyname,
                                      $criteria, $new_object, $options, 
                                      & $succeed,
                                      & $errInfo, 
                                      $mongodb = null)

    {
        $succeed = False;
        $errInfo = '';

        $collection = self::getCollection($keyname, $errInfo, $mongodb);
        if (!$collection) {
            return $ret;
        }

        try {
            $ret = $collection->update($criteria, $new_object, $options);
        } catch (MongoException $e) {
            $errInfo = sprintf("|MongoOperate|Exception|updateData %s %s,%s", 
                                $keyname, $e->getCode(), $e->getMessage());

            return;
        }

        $succeed = True;
        return;
    }

   /**
    * desc: see MongoUpdateBatch
    *       http://php.net/manual/en/class.mongowritebatch.php
    *  
    *
    * params: $keyname like 'url_hits', 'url_dl', see project_conf.php
    *         
    *         $docs, $constructOption, $execOption 
    *
    *         & $succeed
    *         & $errInfo 
    *
    *
    * return:
    **/
    public static function batchUpdateData($keyname, 
                                           & $docs, 
                                           & $succeed,
                                           & $errInfo,
                                           $constructOption = array(),
                                           $execOption = array(),
                                           $mongodb = null)
    {
        $succeed = False;
        $errInfo = '';

        $collection = self::getCollection($keyname, $errInfo, $mongodb);
        if (!$collection) {
            return;
        }

        try {
            $batch = new MongoUpdateBatch($collection, $constructOption);
            foreach ($docs as $doc) {
                $batch->add($doc);
            }

            $batch->execute($execOption);

        } catch (MongoException $e) {
            $errInfo = sprintf("|MongoOperate|Exception|batchUpdateData %s %s,%s", 
                              $keyname, $e->getCode(), $e->getMessage());
            return;
        }

        $succeed = True;
        return;
    } 

    /**
     * desc: 构建形如 $key => array('$regex' => $pattern, '$options' => 'i');
     *
     * params: $query used to receive the query
     *
     */
    public static function getRegexQuery($key, $pattern,
                                         & $query)
    {
        $pattern = str_replace('?', '\?', $pattern);
        $query[$key] = array('$regex' => $pattern, '$options' => 'i');
    }


    /**
     * desc: 构建形如 $key => array('$get' => $low, '$lte' => $high)
     *
     * params: $low, $high can be string
     */ 
    public static function getRangeQuery($key, $low, $high,
                                         $isFloat,
                                         & $query)
    {
        if (empty($low) 
            && empty($high)) {
                return;
            }

        $lowval  = intval($low);
        $highval = intval($high);

        if ($isFloat) {
            $lowval  = floatval($low);
            $highval = floatval($high);
        }     

        if (empty($low)) {
            $query[$key] = array('$lt' => $highval);
            return;
        }

        if (empty($high)) {
            $query[$key] = array('$gte' => $lowval);
            return;
        }

        $query[$key] = array('$gte' => $lowval, '$lt' => $highval);
        return;
    }

    /**
     * desc: 构建形如 $key => array('$where' => 'this.hosts.length > 100 && this.hosts.length < 200')
     *       多用于数组
     *
     * params: $low, $high can be string
     */ 
    public static function getArraySizeRangeQuery($key, $low, $high,
                                                  $isFloat,
                                                  & $query)
    {
        if (empty($low) 
            && empty($high)) {
                return;
            }

        $lowval  = intval($low);
        $highval = intval($high);

        if ($isFloat) {
            $lowval  = floatval($low);
            $highval = floatval($high);
        }     

        if (empty($low)) {
            //$query[$key] = array('$lt' => $highval);
            $query['$where'] = "this.{$key}.length < $highval";
            return;
        }

        if (empty($high)) {
            //$query[$key] = array('$gte' => $lowval);
            $query['$where'] = "this.{$key}.length >= $lowval";
            return;
        }

        //$query[$key] = array('$gte' => $lowval, '$lt' => $highval);
        $query['$where'] = "this.{$key}.length >= $lowval && this.{$key}.length < $highval";
        return;
    }

    public static function getAccQuery($key, $value,
                              & $query)
    {
        $query[$key] = $value;
    }           

    public static function getCount($keyname,
                                    $query, $fields,
                                    & $succeed,
                                    & $retInfo,
                                    $mongodb = null
                                )
    {
        $succeed = False;
        $retInfo = '';

        $collection = self::getCollection($keyname, $retInfo, $mongodb);
        if (!$collection) {
            return;
        }
        
        try {
            $cursor = $collection->find($query, $fields);
            $retInfo = $cursor->count();
        } catch (MongoException $e) {
            $retInfo= sprintf("|MongoOperate|Exception|getcount %s %s,%s", 
                             $keyname, $e->getCode(), $e->getMessage());

            return;
        }

        $succeed = True;
    }

    /**
     * desc: encapsulation for MongoCollection::find,  and MongoCursor related
     *
     * params: $keyname like url_hits, etc, see project_conf
     *         $query, $fields see MongoCollection::find
     *         $options are so MongoCursor, like array('limit'=> limit, 'sort'=> xx)
     *
     *         & $succeed, & $errInfo used to receive operate status, info
     *
     * return: $succeed will be set to True if success, False otherwise
     *         
     *         $retInfo will be set to array, contained the data queried from db if success, otherwise errinfo
     *                
     */ 
     public static function find($keyname,
                                 $query, $fields,
                                 $options,
                                 & $succeed,
                                 & $retInfo,
                                 $mongodb = null,
                                 $timeout = -1
                             )
    {
        $succeed = False;
        $retInfo = '';

        $collection = self::getCollection($keyname, $retInfo, $mongodb);
        if (!$collection) {
            return;
        }
        
        try {
            $cursor = $collection->find($query, $fields);
            $cursor->timeout($timeout);
 
            //set option for cursor
            foreach($options as $key => $value) {
                switch($key)
                {
                case 'limit':
                case 'skip':
                case 'sort':
                    $cursor->$key($value);
                    break;
                default:
                    break;
                }
            }//end foreach
            
            if ($cursor->count(True) > MAX_LIMIT_COUNT) {
                $retInfo = 'Check your query condition, hits too many!!!';
                return;
            }

            $retInfo = array();
            foreach($cursor as $doc) {
                $retInfo[] = $doc;
            }

        } catch (MongoException $e) {
            $retInfo= sprintf("|MongoOperate|Exception|find %s %s,%s", 
                             $keyname, $e->getCode(), $e->getMessage());

            return;
        }

        $succeed = True;
    }

    /**
     * desc: encapsulation for 
     *       public array MongoCollection::findAndModify ( array $query [, array $update [, array $fields [, array $options ]]] )
     *
     *
     * params: $keyname like 'url_hits', 'url_dl', see project_conf
     *         $query, etc, see MongoCollection::findAndModify
     *
     * return: if succeed, $succeed will be set True, and $errInfo indicate the original doc or modified info
     *         if succeed, $succeed will be set False, and $errInfo will indicate error info
     **/
    public static function findAndModify($keyname, 
                                         $query, $update, $fields, $options,
                                         & $succeed,
                                         & $errInfo,
                                         $mongodb = null)
    {
        $succeed = False;
        $errInfo = '';

        $collection = self::getCollection($keyname, $errInfo, $mongodb);
        if (!$collection) {
            return;
        }

        try {
            $errInfo = $collection->findAndModify($query, $update, $fields, $options);

            /*global $g_db_mkiller; 
            $ret = $g_db_mkiller->command(array(
                                        'findAndModify' => 'url_hits',
                                        'query' => $criteria, 
                                        'update' => $new_object,
                                        'fields' => array('_id' => 1),
                                        array('new'   => true,  //return the modified
                                              'upsert' => true)
                                          ));
             */

        } catch (MongoException $e) {
            $errInfo= sprintf("|MongoOperate|Exception|findAndModify %s %s,%s", 
                                $keyname, $e->getCode(), $e->getMessage());
            return;
        }

        $succeed = True;
        return;
    }

    /**
     * desc: 通过聚合，获取某item出现的次数
     *
     * 该方法有关致命的缺陷： exception: aggregation result exceeds maximum document size (16MB)
     *
     * 存在大小限制
     *
     *
     */
    public static function aggGetItemCount($collecname,
                                           $match,  // pipeline,  
                                           $groupid,  //pipeline, 
                                           $outfilter, //pipeline,
                                           $detail,   //see the detail, will be pushed to array, like riskpercent
                                           & $succeed,
                                           & $retInfo,
                                           $project = array(),
                                           $mongodb = null
                                           )
    {
        $succeed = False;
        $errInfo = '';

        $collection = self::getCollection($collecname, $errInfo, $mongodb);
        if (!$collection) {
            return;
        }

        $pipeline = array(
            //only pass thz fields
            /*array(
                '$project' => $project
            ),
             */

            //match
            array(
                '$match' => $match
            ),

            //group
            array(
                '$group' => array('_id' => '$' . $groupid,     //like '_id' => '$key'
                                  'itemCnt' => array('$sum' => 1),
                                  'detail' => array('$addToSet' => '$' . $detail)
                                )              
            ),

            //sort for output
            array(
                '$sort' => array('itemCnt' => -1)
            ),

            //limit for output
            array(
                '$limit' => 50
            ),
            
            //which should output 
            /*array(
                //'$match' => array('itemCnt' => array('$gte' => 8, '$lt' => 12))
                '$match' => $outfilter
            )
            */
        );

        var_dump($pipeline);

        try {
            $retInfo = $collection->aggregate($pipeline);
        } catch (MongoException $e) {
            $retInfo = sprintf("|MongoOperate|Exception|aggGetItemCount %s %s, %s",
                              $collecname, $e->getCode(), $e->getMessage());
            return;
        }

        $succeed = True;
        return;
    }

    /**
     * desc:  list docs indicated by query, fields and limit
     *
     * params: $keyname used for collection, see ./project_conf
     *        
     *        $query, $fields   see MongoCollection::find()
     *        $limits   how many documents to be show 
     *
     * return: direct show info by var_dump
     *
     **/
    public static function listDocs($keyname, 
                                    $mongodb = null,
                                    $query = array(), 
                                    $fields = array(),
                                    $limits = 0,
                                    $timeout = -1)
    {
        $errInfo = '';
        $collection = self::getCollection($keyname, $errInfo, $mongodb);
        if (!$collection) {
            return;
        }

        $cursor = $collection->find();
        $cursor->timeout(-1);

        if ($limits) {
            $cursor->limit($limits);
        }

        echo 'listDocs: ', $keyname, $cursor->count(), "\n";
        foreach($cursor as $doc) {
            var_dump($doc);
        }
    }

    /**
     * desc: get array size for samples, or events, etc
     *       a tool function, change as you need
     *
     * return: directly show info by var_dump
     */
    public static function getArraySize($keyname, $md5_url_ori, $mongodb = null)
    {
        $errInfo = '';
        $collection = self::getCollection($keyname, $errInfo, $mongodb);
        if (!$collection) {
            return;
        }

        //can do within shell, like : db.new_url_hits.find({'month':'2015-12', $where : "this.samples.length > 100"}, {'domain':1, 'url_ori':1})

        // method by aggregate
        $ops = array(
            //match
            array(
                '$match' => array('md5_url_ori' => $md5_url_ori), //'8a63f838f521afd09331b921673f6807'),
            ),

            //size
            array(
                '$project' => array(
                    'month'       => 1,
                    'md5_url_ori' => 1,
                    'url_ori'     => 1,
                    'samplesSize' => array('$size' => '$samples')
                )//end for project
            )
        );

        $ret = $collection->aggregate($ops);
        var_dump($ret);
    }

    /**
     * desc: drop the specified collection by keyname 
     *
     *
     **/
    public static function dropCollection($keyname, $mongodb = null)
    {
        $collection = self::getCollection($keyname, $mongodb);
        if (!$collection) {
            return;
        }

        $collection->drop();
    }
    
    /**
     * desc: get mongodb version
     *
     **/
    public static function getDBVersion()
    {
        global $g_db_mkiller;
        $mongodb_info = $g_db_mkiller->command(array('serverStatus'=>true));
        $mongodb_version = $mongodb_info['version'];
        echo $mongodb_version;
    }

    /**
     * desc: get MongoCollection according to keyname
     *       
     *       need to change the db as you need
     *
     * params: $keyname like new_url_hits, 
     *              more to see project_conf
     *
     *         $errInfo used to receive error info
     *
     * return: MongoCollection if succeed, null otherwise
     *
     **/
    public static function getCollection($keyname,
                                         & $errInfo,
                                         $mongodb = null)
             
    {
        //change as you need
        global $g_db_mkiller;
        global $g_db_conf;

        if (empty($mongodb)) {
            $mongodb = $g_db_mkiller;
        }

        $errInfo    = '';
        $collection = null;
        $ary= $g_db_conf[$keyname];
 
        try {
            //$collection = $g_db_mkiller->selectcollection($ary[0]); 
            $collection = $mongodb->selectcollection($ary[0]);
        } catch (Exception $e) {
            $errInfo = "|MongoOperate|Error|getCollection failed";
            return null;
        }

        return $collection;
    }

    public static function createIndex($keyname, 
                                       $keys, 
                                       & $succeed,
                                       & $errInfo,
                                       $mongodb,
                                       $options = array())
    {
        $succeed = False;
        $errInfo = '';

        $collection = self::getCollection($keyname, $errInfo, $mongodb);
        if (!$collection) {
            return;
        }

        try {
            $collection->createIndex($keys, $options);        
        } catch (MongoException $e) {
            $errInfo = sprintf("|MongoOperate|Exception|createIndex %s %s,%s", 
                              $keyname, $e->getCode(), $e->getMessage());
            return;
        }

        $succeed = True;
        return;
    }
}

/*
testEntry();

function testAggGetItemCount()
{
    global $argv;

    $match = array('date' => array('$gte' => $argv[1], '$lt' => $argv[2]), 
                   'type' => 'path_best',
                   //'riskpercent' => array('$gte' => 0.9)
    );

    $groupid = 'key';
    $detail  = 'riskpercent';
    $project = array('_id' => 0, 'date' => 1, 'type' => 1, 'key' => 1, 'riskpercent' => 1);
    $outfilter = array('itemCnt' => array('$gt' => $argv[3], '$lte' => $argv[4]));

    MongoOperate::aggGetItemCount('stat_info', 
                                  $match,
                                  $groupid,   // group by $key
                                  $outfilter, 
                                  $detail,
                                  $succeed,
                                  $retInfo,
                                  $project);
    if (!$succeed) {
        echo $retInfo;
        return;
    }

    foreach ($retInfo['result'] as $item) {
        $detail = implode("\t", $item['detail']);
        echo "{$item['_id']}\t{$item['itemCnt']}\t{$detail}\n";
    }
}

function testEntry()
{
    $query = array();
    $succeed = False;
    $retInfo = array();

    testAggGetItemCount();
    
    return;
    //MongoOperate::getArraySize('new_url_hits', '8a63f838f521afd09331b921673f6807'); 
}
*/
/*End of file MongoOperate.php*/
