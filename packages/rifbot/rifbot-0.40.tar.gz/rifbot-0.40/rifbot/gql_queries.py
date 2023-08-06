QUERIES = {
    'PING': '''
        query {
            ping
        }
        ''',

    'FIND_ONE_STRATEGY_ARCHIVE':
        '''
        query ($options: JSON){
            findOneStrategyRun(options: $options){
                id
                runId
                registrarEntry {
                    id
                    name
                    host
                    hostName
                    port
                    processName
                    localIp
                    publicIp
                    features {
                      name
                      data
                    }
                    summary
                }
                status {
                    topic
                    data
                }
                rootOptions {
                    runType
                    strategy {
                        label
                        value
                    }
                    startPaused
                    exchange {
                        id
                        owner
                        label
                        type
                    }
                    symbol {
                        asset
                        currency
                    }
                    timeFrame {
                        label
                        minutes
                    }
                    start
                    end
                    daylightSavings
                    liveOnly
                    initialCapital
                    repartition
                    warmUpCandleCount
                    EMALength
                    ATRLength
                    enterPeriod
                    closePeriod
                    includeCurrentCandlestick
                    ATRPhi
                    ATRMuSigma
                    pyramiding
                    NStepUp
                    NStepStop
                    buyLeverage
                    sellLeverage
                    moneyMgtPercentage
                    capitalFloorPercentage
                    hardCapSize
                }
                sequentialCandles {
                    i
                    b {
                      cf
                      rcf
                      cl
                      ana
                      pe
                    }
                    c {
                      i
                      ohlc
                      d
                      tc
                    }
                    ind
                    ps
                }
            }
        }
        '''
}

MUTATIONS = {
    'ENQUEUE_STRATEGY_RUN':
        '''
        mutation($rootOptions: RootOptionsInput!, $runId: String) {
            enqueueStrategyRun(rootOptions: $rootOptions, runId: $runId) {
                type
                status
                createdTs
                startedTs
                endedTs
                args
                executor {
                    id
                    name
                    host
                    hostName
                    port
                    processName
                    localIp
                    publicIp
                    features {
                      name
                      data
                    }
                    summary
                }  
            }
        }
    '''
}

SUBSCRIPTIONS = {
    'PING': '''
        subscription {
            ping
        }
    ''',
}
