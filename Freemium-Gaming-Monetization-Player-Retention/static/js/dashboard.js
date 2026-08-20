$(function () {
    $('.select2').select2({
        width: '100%',
        placeholder: 'All values',
        closeOnSelect: false
    });

    const chartIds = [
        'chart-pareto', 'chart-genre-rev', 'chart-depth', 'chart-segment-revenue',
        'chart-corr', 'chart-scatter', 'chart-session-box', 'chart-engagement',
        'chart-device', 'chart-device-revenue', 'chart-country', 'chart-country-arpu',
        'chart-gender-genre', 'chart-age', 'chart-latency'
    ];

    function payload() {
        return {
            genres: $('#genres').val() || [],
            segments: $('#segments').val() || [],
            devices: $('#devices').val() || [],
            countries: $('#countries').val() || []
        };
    }

    function selectedLabels() {
        const p = payload();
        return [
            ...p.genres.map(x => ['Genre', x]),
            ...p.segments.map(x => ['Segment', x]),
            ...p.devices.map(x => ['Device', x]),
            ...p.countries.map(x => ['Country', x])
        ];
    }

    function updateSelectionUI() {
        const labels = selectedLabels();
        const box = $('#active-filters').empty();
        const chips = $('#selection-chips').empty();

        if (!labels.length) {
            box.html('<span class="muted">No filters selected — showing the full dataset</span>');
            $('#filter-status').text('All data');
            $('#selection-title').text('All players');
            return;
        }

        labels.forEach(([type, value]) => {
            const chip = `<span class="active-chip"><b>${escapeHtml(type)}:</b> ${escapeHtml(value)}</span>`;
            box.append(chip);
            chips.append(chip);
        });

        $('#filter-status').text(labels.length + ' active');
        $('#selection-title').text('Filtered player population');
    }

    function escapeHtml(value) {
        return $('<div>').text(value == null ? '' : value).html();
    }

    function showLoading() { $('#loading').addClass('show'); }
    function hideLoading() { $('#loading').removeClass('show'); }

    function renderChart(id, fig) {
        const el = document.getElementById(id);
        if (!el) return;

        if (!fig || !fig.data) {
            el.innerHTML = '<div style="padding:60px;text-align:center;color:#69768a;font-size:12px">No data available for this selection.</div>';
            return;
        }

        const palette = [
            '#FF8A3D', '#5DA9FF', '#45D483', '#A78BFA',
            '#4DD8E8', '#FF5C8A', '#F6C85F', '#8B9CF6',
            '#22C1A1', '#F97316'
        ];

        const piePalette = [
            '#FF8A3D', '#5DA9FF', '#45D483', '#A78BFA',
            '#4DD8E8', '#FF5C8A', '#F6C85F', '#8B9CF6'
        ];

        const data = fig.data.map((trace, i) => {
            const t = { ...trace };

            if (t.type === 'bar') {
                t.marker = {
                    ...(t.marker || {}),
                    color: palette[i % palette.length],
                    line: { color: 'rgba(255,255,255,.10)', width: 1 },
                    cornerradius: 6
                };
                t.opacity = 0.92;
                t.hovertemplate = t.hovertemplate || '%{x}<br><b>%{y}</b><extra></extra>';
            }

            if (t.type === 'pie') {
                t.marker = {
                    ...(t.marker || {}),
                    colors: piePalette,
                    line: { color: '#0b1018', width: 2 }
                };
                t.hole = 0.56;
                t.textfont = { color: '#F4F7FB', size: 11 };
                t.hovertemplate = '%{label}<br><b>%{percent}</b><extra></extra>';
            }

            if (t.type === 'scatter') {
                t.marker = {
                    ...(t.marker || {}),
                    color: palette[i % palette.length],
                    size: 8,
                    opacity: 0.72,
                    line: { color: 'rgba(255,255,255,.35)', width: 1 }
                };
                if (t.mode && t.mode.includes('lines')) {
                    t.line = { ...(t.line || {}), color: palette[i % palette.length], width: 3 };
                }
            }

            if (t.type === 'histogram') {
                t.marker = {
                    ...(t.marker || {}),
                    color: palette[i % palette.length],
                    line: { color: 'rgba(255,255,255,.14)', width: 1 }
                };
                t.opacity = 0.82;
            }

            if (t.type === 'box') {
                t.marker = { ...(t.marker || {}), color: palette[i % palette.length] };
                t.line = { ...(t.line || {}), color: palette[i % palette.length], width: 2 };
                t.fillcolor = 'rgba(93,169,255,.16)';
                t.opacity = 0.9;
            }

            return t;
        });

        const layout = {
            ...fig.layout,
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: {
                ...(fig.layout.font || {}),
                color: '#DDE5F0',
                family: 'Inter, system-ui, sans-serif'
            },
            title: {
                ...(fig.layout.title || {}),
                font: { color: '#F3F6FA', size: 14 }
            },
            colorway: palette,
            hoverlabel: {
                bgcolor: '#111A26',
                bordercolor: '#33435A',
                font: { color: '#F7FAFC', size: 12 }
            },
            xaxis: {
                ...(fig.layout.xaxis || {}),
                color: '#8E9AAC',
                gridcolor: 'rgba(255,255,255,.055)',
                linecolor: 'rgba(255,255,255,.08)',
                zerolinecolor: 'rgba(255,255,255,.08)'
            },
            yaxis: {
                ...(fig.layout.yaxis || {}),
                color: '#8E9AAC',
                gridcolor: 'rgba(255,255,255,.055)',
                linecolor: 'rgba(255,255,255,.08)',
                zerolinecolor: 'rgba(255,255,255,.08)'
            },
            legend: {
                ...(fig.layout.legend || {}),
                bgcolor: 'rgba(10,15,23,.65)',
                bordercolor: 'rgba(255,255,255,.08)',
                borderwidth: 1,
                font: { color: '#C8D2DF', size: 10 }
            },
            margin: { l: 48, r: 24, t: 48, b: 48 },
            height: 360,
            transition: { duration: 450, easing: 'cubic-in-out' }
        };

        el.style.opacity = '0';
        el.style.transform = 'translateY(8px) scale(.985)';
        el.style.transition = 'opacity .42s ease, transform .42s cubic-bezier(.2,.8,.2,1)';

        Plotly.react(el, data, layout, {
            responsive: true,
            displaylogo: false,
            displayModeBar: false
        }).then(() => {
            requestAnimationFrame(() => {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0) scale(1)';
            });
        });
    }

    function renderTable(columns, rows, total) {
        $('#table-head-row').empty();
        $('#table-body').empty();
        $('#table-summary').text(`${Number(total || 0).toLocaleString()} records`);

        if (!columns || !rows || !rows.length) {
            $('#table-body').html('<tr><td colspan="20" style="text-align:center;padding:30px;color:#69768a">No records match the selected filters.</td></tr>');
            return;
        }

        columns.forEach(c => $('#table-head-row').append(`<th>${escapeHtml(c)}</th>`));
        rows.forEach(row => {
            let html = '<tr>';
            columns.forEach(c => {
                html += `<td>${escapeHtml(row[c] == null ? '-' : row[c])}</td>`;
            });
            html += '</tr>';
            $('#table-body').append(html);
        });
    }

    function updateDashboard() {
        updateSelectionUI();
        showLoading();

        $.ajax({
            url: '/api/filter',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(payload()),
            success: function (res) {
                $('#kpi-revenue').text(res.kpis.total_revenue);
                $('#kpi-paying').text(res.kpis.paying_users);
                $('#kpi-f2p').text(res.kpis.f2p_users);
                $('#kpi-arppu').text(res.kpis.arppu);
                $('#kpi-conversion').text(res.kpis.conversion_rate);
                $('#kpi-sessions').text(res.kpis.avg_sessions);
                $('#row-count').text(Number(res.row_count || 0).toLocaleString() + ' players');

                // Render Dynamic Key Insights Panel
                const $insightsList = $('#key-insights-list').empty();
                if (res.insights && res.insights.length) {
                    res.insights.forEach(item => {
                        $insightsList.append(
                            `<li style="background: rgba(17, 26, 39, 0.7); border: 1px solid #243349; border-left: 3px solid var(--orange); border-radius: 8px; padding: 10px 14px; line-height: 1.5;">${item}</li>`
                        );
                    });
                } else {
                    $insightsList.html('<li style="color:#687487;">No specific insights available for this subset.</li>');
                }

                // Render Charts
                renderChart('chart-pareto', res.charts.fig_pareto);
                renderChart('chart-genre-rev', res.charts.fig_genre_rev);
                renderChart('chart-depth', res.charts.fig_depth);
                renderChart('chart-segment-revenue', res.charts.fig_segment_revenue);
                renderChart('chart-corr', res.charts.fig_corr);
                renderChart('chart-scatter', res.charts.fig_scatter);
                renderChart('chart-session-box', res.charts.fig_session_box);
                renderChart('chart-engagement', res.charts.fig_engagement);
                renderChart('chart-device', res.charts.fig_device);
                renderChart('chart-device-revenue', res.charts.fig_device_revenue);
                renderChart('chart-country', res.charts.fig_country);
                renderChart('chart-country-arpu', res.charts.fig_country_arpu);
                renderChart('chart-gender-genre', res.charts.fig_gender_genre);
                renderChart('chart-age', res.charts.fig_age);
                renderChart('chart-latency', res.charts.fig_latency);
                renderTable(res.table_cols, res.table_data, res.row_count);
            },
            error: function (xhr) {
                console.error(xhr.responseText || xhr);
                alert('Could not update the dashboard. Check the Flask terminal for the error.');
            },
            complete: hideLoading
        });
    }

    $('#apply-filters-btn').on('click', updateDashboard);

    $('#reset-filters-btn').on('click', function () {
        $('.select2').val(null).trigger('change');
        updateDashboard();
    });

    $('#download-csv-btn').on('click', function () {
        const btn = $(this);
        const original = btn.text();
        btn.text('Preparing…').prop('disabled', true);

        fetch('/api/download-csv', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload())
        })
            .then(r => {
                if (!r.ok) throw new Error('Download failed');
                return r.blob();
            })
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'freemium_game_analytics_filtered.csv';
                a.click();
                URL.revokeObjectURL(url);
            })
            .catch(console.error)
            .finally(() => btn.text(original).prop('disabled', false));
    });

    $('.tab-btn').on('click', function () {
        $('.tab-btn').removeClass('active');
        $('.tab-panel').removeClass('active');
        $(this).addClass('active');
        $('#panel-' + $(this).data('tab')).addClass('active');
        window.dispatchEvent(new Event('resize'));
    });

    $('#mobile-menu-btn').on('click', function () {
        $('#sidebar').addClass('open');
        $('#mobile-overlay').addClass('show');
    });
    $('#mobile-overlay').on('click', function () {
        $('#sidebar').removeClass('open');
        $(this).removeClass('show');
    });

    $('.select2').on('change', updateSelectionUI);

    updateSelectionUI();
    updateDashboard();
});

$('#ask-ai-btn').on('click', function () {
    const $btn = $(this);
    const $container = $('#ai-response-container');

    $btn.text('Analyzing...').prop('disabled', true);
    $container.html('<span class="muted">Generating cohort intelligence via LLM...</span>');

    $.ajax({
        url: '/api/ai-insights',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(payload()),
        success: function (res) {
            // Converts line breaks to HTML formatting
            $container.html(res.ai_summary.replace(/\n/g, '<br>'));
        },
        error: function () {
            $container.html('<span style="color:#ff5c8a;">Failed to load AI summary.</span>');
        },
        complete: function () {
            $btn.text('Generate AI Analysis').prop('disabled', false);
        }
    });
});

document.addEventListener('click', function (event) {
    const target = event.target.closest('button,.btn,.download-btn,.tab-btn');
    if (!target) return;
    target.classList.remove('click-feedback');
    void target.offsetWidth;
    target.classList.add('click-feedback');
    setTimeout(() => target.classList.remove('click-feedback'), 220);
});