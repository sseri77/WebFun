// common.js
const API_URL = "https://script.google.com/macros/s/AKfycbzteDdUYyf-DF3Rvf1ba-Hw20Id-aQZbHq8zp2FUVykb4fWa8StJaodEFCeFOVLIZTl0A/exec";

/**
 * 전 서버 데이터 로드
 */
async function fetchAllData() {
    try {
        const res = await fetch(API_URL);
        return await res.json();
    } catch (e) {
        console.error("데이터 로드 실패:", e);
        return null;
    }
}

/**
 * 핵심 차감 로직: 모든 단계의 데이터를 합산하여 선수별 잔량 계산
 */
function getInventorySummary(db) {
    const summary = {};
    const getKey = (i) => `${i.team}|${i.collab}|${i.num}|${i.name}`;

    db.inbound.forEach(i => {
        const k = getKey(i);
        if(!summary[k]) summary[k] = { in:0, proc:0, out:0, lastIdx: i.idx };
        summary[k].in += Number(i.qty);
    });
    db.process.forEach(i => {
        const k = getKey(i);
        if(!summary[k]) summary[k] = { in:0, proc:0, out:0, lastIdx: i.idx };
        summary[k].proc += Number(i.qty);
        summary[k].lastIdx = i.idx;
    });
    db.outbound.forEach(i => {
        const k = getKey(i);
        if(!summary[k]) summary[k] = { in:0, proc:0, out:0, lastIdx: i.idx };
        summary[k].out += Number(i.qty);
        summary[k].lastIdx = i.idx;
    });
    return summary;
}

/**
 * 데이터 전송 공통 함수 (INSERT, UPDATE, DELETE)
 */
aasync function sendData(payload) {
    // no-cors를 제거해야 GAS에서 데이터를 안정적으로 파싱합니다.
    return fetch(API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'text/plain' // JSON 대신 text/plain으로 보내야 CORS 에러를 피하면서 GAS가 잘 읽습니다.
        },
        body: JSON.stringify(payload)
    });
}


/**
 * 공통 네비게이션 바 생성 (모든 페이지 상단에 자동 삽입 가능)
 */
function injectNavbar(activePage) {
    const navHtml = `
        <header class="mb-6 flex justify-between items-center border-b border-gray-700 pb-4">
            <h1 class="text-xl font-black text-blue-400 font-mono tracking-tighter">MARKING-KIT OPS</h1>
            <div class="flex gap-4 text-[11px] font-bold uppercase">
                <a href="index.html" class="${activePage==='index'?'text-white':'text-gray-500'}">메인</a>
                <a href="inbound.html" class="${activePage==='inbound'?'text-blue-400':'text-gray-500'}">입고</a>
                <a href="process.html" class="${activePage==='process'?'text-yellow-500':'text-gray-500'}">재단</a>
                <a href="outbound.html" class="${activePage==='outbound'?'text-red-500':'text-gray-500'}">출고</a>
            </div>
        </header>
    `;
    document.body.insertAdjacentHTML('afterbegin', `<div class="max-w-5xl mx-auto pt-4">${navHtml}</div>`);
}
