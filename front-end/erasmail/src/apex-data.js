const radialBarPotentialImpact = {
    chart: {
        height: 280,
        type: "radialBar",
    },
    series: [44, 55, 67],
    colors: ["hsl(141, 71%, 48%)"],
    plotOptions: {
        radialBar: {
            track: {
                background: "hsl(48, 100%, 67%)",
                opacity: 0.4,
            },
            dataLabels: {
                name: {
                    fontSize: "22px",
                    color: ["hsl(217, 71%, 53%)"]
                },
                value: {
                    fontSize: "16px",
                    formatter: function (val) {
                        return val + '% saved'
                    }
                },
                total: {
                    show: true,
                    label: "Currently saved",
                    formatter: function (w) {
                        return (
                            (
                                w.globals.seriesTotals.reduce((a, b) => {
                                    return a + b;
                                }, 0) / w.globals.series.length
                            ).toPrecision(2) + "% / Total potential"
                        );
                    },
                },
            },
        },
    },
    labels: ["Newsletters", "E-mails", "CO2"],
}

const lineSizeMailbox = {
    chartOptions: {
        chart: {
            id: "vuechart-example",
        },
        xaxis: {
            categories: ["Before ErasMail", "13/03/2021"],
        },
    },
    series: [
        {
            name: "series-1",
            data: [6, 4],
        },
    ]
}

export { radialBarPotentialImpact, lineSizeMailbox }