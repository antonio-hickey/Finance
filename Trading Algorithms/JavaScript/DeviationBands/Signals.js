/*
      Antonio Hickey (https://git.io/J3BnG)
     ----------------------------------------------
     | Signals for VWAP Deviation Bands           | 
     ----------------------------------------------
         - Bull Trending Signal = price > (VWAP + sigma)
         - Bull Reversion Signal = price > VWAP && price < (VWAP + sigma)

         - Bear Trending Signal = price < (VWAP - sigma)
         - Bear Reversion Signal = price < VWAP && price > (VWAP - sigma)
     ----------------------------------------------
*/

//
const predef = require("./tools/predef");
const meta = require("./tools/meta");
const medianPrice = require("./tools/typicalPrice");
const { ParamType } = meta;
//

// Volume Type
const volType = {
    vol: 'volume',
    askVol: 'offerVolume',
    bidVol: 'bidVolume'
}
//

// Module for rolling period
function num(defValue,step,min) {
    return {
        type: ParamType.NUMBER,
        def: defValue,
        restrictions: {
            step: step || 1,
            min: min > 0 ? min : 0
        }
    };
}
//

// Class
class Signals {
    init() {
        this.cumulativeVolume = 0;
        this.cumulativeValue = 0;
        this.cumulativeValue2 = 0;
        this.tradeDate = 0;
        this.vwaps = [];
    }
    // Start of function
    map(d,i,history) {
        
        // Start of loop
        if (d.tradeDate) {
            // Input Values
            const tradeDate = d.tradeDate();
            const period = this.props.rollingPeriod + 1
            const pastData = history.data[i-period]
            //

            // If historic data
            if (pastData) {
                const pastProfile = pastData.profile()
                if (pastProfile && pastProfile.length) {
                    for (let i=0; i<pastProfile.length; ++i) {
                        const level = pastProfile[i];
                        const vol = level[this.props.vol];
                        this.cumulativeVolume -= vol;
                        this.cumulativeValue -= vol * level.price;
                        this.cumulativeValue2 -= vol * Math.pow(level.price,2);
                    }
                } else {
                    const vol = pastData[volType[this.props.vol]]();
                    this.cumulativeVolume -= vol;
                    this.cumulativeValue -= vol * medianPrice(pastData);
                    this.cumulativeValue2 -= vol * Math.pow(medianPrice(pastData),2);
                }
            }
            //

            // Else live data
            const volumeProfile = d.profile();
            if (volumeProfile && volumeProfile.length) {
                for (let i = 0; i < volumeProfile.length; ++i) {
                    const level = volumeProfile[i];
                    this.cumulativeVolume += level.vol;
                    this.cumulativeValue += level.vol * level.price;
                    this.cumulativeValue2 += level.col * Math.pow(level.price,2);
                }
            }
            else {
                const vol = d.volume();
                this.cumulativeVolume += vol;
                this.cumulativeValue += vol * medianPrice(d);
                this.cumulativeValue2 += vol * Math.pow(medianPrice(d),2);
            }
            //

            // VWAP Deviation Bands
            const vwap = this.cumulativeValue / this.cumulativeVolume;
            const sigma = Math.sqrt(Math.max(this.cumulativeValue2 / this.cumulativeVolume - Math.pow(vwap,2),0));
            const bull_sup = vwap + sigma;
            const bull_res = vwap + (sigma * 2);
            const bull_cap = vwap + (sigma * 3);
            const bear_sup = vwap - sigma;
            const bear_res = vwap - (sigma * 2);
            const bear_cap = vwap - (sigma * 3);
            //

            // Signals
            let BullTrendingSignal;
            let BullReversionSignal;
            let BearTrendingSignal;
            let BearReversionSignal;
            //

            // Input values
            const tickSize = this.contractInfo.tickSize;
            const price = d.value();
            //

            // Bull Signals
            if (price >= bull_sup) {
                BullTrendingSignal = d.low() - (tickSize*this.props.plotInTick);
            }
            if (price > vwap && price < bull_sup) {
                BullReversionSignal = d.high() + (tickSize*this.props.plotInTick);
            }
            //

            // Bear Signals
            if (price <= bear_sup) {
                BearTrendingSignal = d.high() + (tickSize*this.props.plotInTick);
            }
            if (price < vwap && price > bear_sup) {
                BearReversionSignal = d.low() - (tickSize*this.props.plotInTick);
            }
            //
            
            // Output
            return {
                BullTrendingSignal: BullTrendingSignal,
                BullReversionSignal: BullReversionSignal,
                BearTrendingSignal: BearTrendingSignal,
                BearReversionSignal: BearReversionSignal
            }
            //
        }
    }
}
//
// Exporting Modules
module.exports = {
    name: "Signals",
    description: "Signals",
    calculator: Signals,
    inputType: meta.InputType.BARS,
    tags: ["My Indicators"],
    params: {
        plotInTick: predef.paramSpecs.number(2),
        vol: predef.paramSpecs.enum({
            vol: 'Volume',
            bidVol: 'Bid Volume',
            askVol: 'Ask Volume',
        }, 'vol'),
        rollingPeriod: num(30,1,1)
    },
    plotter: [
        predef.plotters.dots('BearTrendingSignal'),
        predef.plotters.dots('BearReversionSignal'),
        predef.plotters.dots('BullTrendingSignal'),
        predef.plotters.dots('BullReversionSignal')
    ],
    plots: {
        BearTrendingSignal: { title: "Bearish Trend" },
        BearReversionSignal: { title: "Bearish Trend" },
        BullTrendingSignal: { title: "Bullish Trend" },
        BullReversionSignal: { title: "Bullish Reversion" }
    },
    schemeStyles: {
        dark: {
            BearTrendingSignal: {color: "red"},
            BearReversionSignal: {color: "blue"},
            BullTrendingSignal: {color: "green"},
            BullReversionSignal: {color: "blue"}
        },
        light: {
            BearTrendingSignal: {color: "red"},
            BearReversionSignal: {color: "blue"},
            BullTrendingSignal: {color: "green"},
            BullReversionSignal: {color: "blue"}
        }
    }
};
//
