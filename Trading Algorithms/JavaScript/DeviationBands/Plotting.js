/*
    Antonio Hickey (https://github.com/antonio-hickey)
    
    Javascript for use with Tradovate:

    Volume Weighted Average Price Standard Deviation Bands
    ----------------------------------------------------------
        - Bull and Bear Value, rolling VWAP
        - Bull and Bear Support, rolling VWAP * (1 sigma)
        - Bull and Bear Resistance, rolling VWAP * (2 sigma)
        - Bull and Bear Capitulation, rolling VWAP * (3 sigma)
    ----------------------------------------------------------
*/
const predef = require("./tools/predef");
const meta = require("./tools/meta");
const medianPrice = require("./tools/typicalPrice");
const { ParamType } = meta;

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
class stdBands {
    init() {
        this.cumulativeVolume = 0;
        this.cumulativeValue = 0;
        this.cumulativeValue2 = 0;
        this.tradeDate = 0;
        this.vwaps = [];
    }
    
    map(d,i,history) {
        if (d.tradeDate) {
            const tradeDate = d.tradeDate();
            const period = this.props.rollingPeriod + 1
            const pastData = history.data[i-period]
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

            const vwap = this.cumulativeValue / this.cumulativeVolume;
            const stdDev = Math.sqrt(Math.max(this.cumulativeValue2 / this.cumulativeVolume - Math.pow(vwap,2),0));
            const bull_sup = vwap + stdDev;
            const bull_res = vwap + (stdDev * 2);
            const bull_cap = vwap + (stdDev * 3);
            const bear_sup = vwap - stdDev;
            const bear_res = vwap - (stdDev * 2);
            const bear_cap = vwap - (stdDev * 3);

            // Output
            return {
                vwap: vwap,
                bull_sup: bull_sup,
                bull_res: bull_res,
                bull_cap: bull_cap,
                bear_sup: bear_sup,
                bear_res: bear_res,
                bear_cap: bear_cap
            }
            //
        }
    }
}
//

// Exporting Modules
module.exports = {
    name: "stdBands",
    description: "VWAPBANDS",
    calculator: stdBands,
    inputType: meta.InputType.BARS,
    tags: ["My Indicators"],
    params: {
        vol: predef.paramSpecs.enum({
            vol: 'Volume',
            bidVol: 'Bid Volume',
            askVol: 'Ask Volume',
        }, 'vol'),
        rollingPeriod: num(30,1,1)
    },
    plots: {
        vwap: { title: "Rolling VWAP" },
        bull_sup: { title: "Bull Support" },
        bull_res: { title: "Bull Resistance" },
        bull_cap: { title: "Bull Capitulation" },
        bear_sup: { title: "Bear Support" },
        bear_res: { title: "Bear Resistance" },
        bear_cap: { title: "Bear Capitulation" },
    },
    schemeStyles: {
        dark: {
            vwap: predef.styles.plot({color: "#50E3C2", lineStyle:1, lineWidth:5}),
            bull_sup: predef.styles.plot({color: "#F8E71C", lineStyle:3, lineWidth:2}),
            bull_res: predef.styles.plot({color: "#F5A623", lineStyle:1, lineWidth:2}),
            bull_cap: predef.styles.plot({color: "#D0021B", lineStyle:3}),
            bear_sup: predef.styles.plot({color: "#F8E71C", lineStyle:3, lineWidth:2}),  
            bear_res: predef.styles.plot({color: "#F5A623", lineStyle:1, lineWidth:2}),  
            bear_cap: predef.styles.plot({color: "#D0021B", lineStyle:3})
        },
        light: {
            vwap: predef.styles.plot({color: "#50E3C2", lineStyle:1, lineWidth:5}),
            bull_sup: predef.styles.plot({color: "#F8E71C", lineStyle:3, lineWidth:2}),
            bull_res: predef.styles.plot({color: "#F5A623", lineStyle:3, lineWidth:2}),
            bull_cap: predef.styles.plot({color: "#D0021B", lineStyle:3}),      
            bear_sup: predef.styles.plot({color: "#F8E71C", lineStyle:3, lineWidth:2}),  
            bear_res: predef.styles.plot({color: "#F5A623", lineStyle:1, lineWidth:2}),  
            bear_cap: predef.styles.plot({color: "#D0021B", lineStyle:3})
        }
    }
};
//
