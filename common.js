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
