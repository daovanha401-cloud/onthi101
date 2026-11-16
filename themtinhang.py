# -*- coding: utf-8 -*-
"""
==============================================================
  WEB ÔN THI TUYỂN SINH VÀO LỚP 10 — TOÁN · NGỮ VĂN · TIẾNG ANH
  - Lý thuyết trọng tâm 3 môn
  - Luyện đề trắc nghiệm có bấm giờ, chấm điểm, lời giải
  - Tiếng Anh: LUYỆN NGHE (máy đọc) + LUYỆN NÓI (nhận diện giọng nói)
  - ĐĂNG NHẬP / ĐĂNG KÝ tài khoản người dùng
--------------------------------------------------------------
  Chỉ dùng thư viện có sẵn của Python, KHÔNG cần cài thêm gì.
  Chạy:  python thi_vao_10.py   -> mở http://localhost:8000
  Lưu ý: Luyện nói nên dùng Google Chrome hoặc Microsoft Edge,
         cho phép dùng micro và cần có kết nối Internet.
  TRỢ LÝ AI (tùy chọn): cài thư viện  ->  pip install anthropic
         rồi dán khóa API vào biến API_KEY bên dưới (hoặc đặt biến
         môi trường ANTHROPIC_API_KEY). Không có khóa thì trợ lý
         vẫn chạy ở chế độ offline (tra cứu lý thuyết có sẵn).
==============================================================
"""
import html
import json
import os
import random
import re
import threading
import webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

PORT = 8000
NGAY_THI = "2027-06-01"   # Ngày thi dự kiến (sửa theo tỉnh/thành của bạn)

# ---- Cấu hình TRỢ LÝ AI ----
API_KEY = ""                 # Dán khóa API Anthropic vào giữa hai dấu ngoặc kép (KHÔNG chia sẻ file khi đã dán khóa)
MODEL_AI = "claude-opus-5-5" # Mô hình AI sử dụng

# ==============================================================
# 1. LÝ THUYẾT
# ==============================================================
LY_THUYET = {
    "toan": [
        {"ten": "Căn bậc hai & Căn thức", "noi_dung": """
<ul>
<li>√A xác định ⇔ <b>A ≥ 0</b></li>
<li>√(A²) = |A|</li>
<li>√(A·B) = √A · √B &nbsp;(A, B ≥ 0)</li>
<li>√(A/B) = √A / √B &nbsp;(A ≥ 0, B &gt; 0)</li>
<li>Trục căn ở mẫu: <span class="ct">A/√B = A√B / B</span></li>
<li>Liên hợp: <span class="ct">1/(√a − √b) = (√a + √b)/(a − b)</span></li>
</ul>
<div class="vd"><b>Ví dụ:</b> √50 − √18 = 5√2 − 3√2 = <b>2√2</b></div>"""},
        {"ten": "Hàm số bậc nhất y = ax + b", "noi_dung": """
<ul>
<li>Là hàm bậc nhất khi <b>a ≠ 0</b>. Đồng biến khi a &gt; 0, nghịch biến khi a &lt; 0.</li>
<li>Đồ thị là đường thẳng cắt trục tung tại (0; b).</li>
<li>Hai đường thẳng y = ax + b và y = a'x + b':
  <ul><li>Song song ⇔ a = a', b ≠ b'</li>
  <li>Trùng nhau ⇔ a = a', b = b'</li>
  <li>Cắt nhau ⇔ a ≠ a'</li>
  <li>Vuông góc ⇔ a·a' = −1</li></ul></li>
</ul>"""},
        {"ten": "Hàm số y = ax² (a ≠ 0)", "noi_dung": """
<ul>
<li>a &gt; 0: đồ thị (parabol) quay bề lõm lên, giá trị nhỏ nhất y = 0 tại x = 0.</li>
<li>a &lt; 0: parabol quay bề lõm xuống, giá trị lớn nhất y = 0 tại x = 0.</li>
<li>Giao của parabol y = ax² và đường thẳng y = mx + n: giải <span class="ct">ax² = mx + n</span>
  <ul><li>Δ &gt; 0: cắt tại 2 điểm · Δ = 0: tiếp xúc · Δ &lt; 0: không giao</li></ul></li>
</ul>"""},
        {"ten": "Phương trình bậc hai & Hệ thức Vi-ét", "noi_dung": """
<p>Phương trình <span class="ct">ax² + bx + c = 0 (a ≠ 0)</span>, <span class="ct">Δ = b² − 4ac</span></p>
<ul>
<li>Δ &gt; 0: hai nghiệm phân biệt <span class="ct">x = (−b ± √Δ) / 2a</span></li>
<li>Δ = 0: nghiệm kép x = −b/2a · Δ &lt; 0: vô nghiệm</li>
<li>Nếu b = 2b' dùng Δ' = b'² − ac cho gọn.</li>
<li><b>Vi-ét:</b> <span class="ct">x₁ + x₂ = −b/a</span> ; <span class="ct">x₁·x₂ = c/a</span></li>
<li>Nhẩm nghiệm: a + b + c = 0 ⇒ x = 1, x = c/a ; a − b + c = 0 ⇒ x = −1, x = −c/a</li>
<li>x₁² + x₂² = (x₁ + x₂)² − 2x₁x₂</li>
</ul>
<div class="vd"><b>Ví dụ:</b> x² − 5x + 4 = 0 có 1 − 5 + 4 = 0 ⇒ x = 1; x = 4</div>"""},
        {"ten": "Hệ hai phương trình bậc nhất hai ẩn", "noi_dung": """
<ul>
<li><b>Phương pháp thế:</b> rút một ẩn từ một phương trình rồi thế vào phương trình còn lại.</li>
<li><b>Phương pháp cộng đại số:</b> nhân hệ số để một ẩn đối nhau rồi cộng vế theo vế.</li>
<li>Hệ ax + by = c ; a'x + b'y = c' có nghiệm duy nhất khi a/a' ≠ b/b'.</li>
</ul>
<div class="vd"><b>Giải bài toán bằng cách lập hệ:</b> đặt ẩn và điều kiện → lập hệ → giải → đối chiếu điều kiện → kết luận.</div>"""},
        {"ten": "Hệ thức lượng trong tam giác vuông", "noi_dung": """
<p>Tam giác ABC vuông tại A, đường cao AH, BC = a, AC = b, AB = c:</p>
<ul>
<li><span class="ct">a² = b² + c²</span> (Pi-ta-go)</li>
<li><span class="ct">b² = a·b'</span> ; <span class="ct">c² = a·c'</span></li>
<li><span class="ct">h² = b'·c'</span> ; <span class="ct">a·h = b·c</span></li>
<li><span class="ct">1/h² = 1/b² + 1/c²</span></li>
<li>sin = đối/huyền · cos = kề/huyền · tan = đối/kề · cot = kề/đối</li>
</ul>"""},
        {"ten": "Đường tròn & Góc", "noi_dung": """
<ul>
<li>Góc ở tâm = số đo cung bị chắn.</li>
<li>Góc nội tiếp = ½ số đo cung bị chắn. Góc nội tiếp chắn nửa đường tròn = <b>90°</b>.</li>
<li>Góc tạo bởi tia tiếp tuyến và dây cung = ½ cung bị chắn.</li>
<li><b>Tứ giác nội tiếp</b> ⇔ tổng hai góc đối = 180° hoặc hai đỉnh kề cùng nhìn một cạnh dưới hai góc bằng nhau.</li>
<li>Tiếp tuyến vuông góc với bán kính tại tiếp điểm.</li>
<li>Độ dài đường tròn C = 2πR · Diện tích S = πR²</li>
</ul>"""},
        {"ten": "Hình trụ – Hình nón – Hình cầu", "noi_dung": """
<table class="bang"><tr><th>Hình</th><th>Diện tích xung quanh</th><th>Thể tích</th></tr>
<tr><td>Trụ</td><td>2πrh</td><td>πr²h</td></tr>
<tr><td>Nón</td><td>πrl</td><td>⅓πr²h</td></tr>
<tr><td>Cầu</td><td>S = 4πR²</td><td>⁴⁄₃πR³</td></tr></table>"""},
    ],
    "van": [
        {"ten": "Cấu trúc đề thi Ngữ văn", "noi_dung": """
<ul>
<li><b>Phần I – Đọc hiểu:</b> văn bản (thường ngoài SGK), hỏi về thể loại, phương thức biểu đạt, biện pháp tu từ, nội dung, thông điệp.</li>
<li><b>Phần II – Viết:</b>
  <ul><li>Đoạn văn nghị luận văn học (khoảng 200 chữ) hoặc nghị luận xã hội.</li>
  <li>Bài văn nghị luận (xã hội hoặc văn học).</li></ul></li>
</ul>
<div class="vd">💡 Từ năm 2025 đề thi theo Chương trình 2018 dùng nhiều văn bản ngoài sách giáo khoa — hãy học <b>kỹ năng đọc theo thể loại</b> thay vì học thuộc lòng.</div>"""},
        {"ten": "Các biện pháp tu từ", "noi_dung": """
<table class="bang"><tr><th>Biện pháp</th><th>Dấu hiệu</th><th>Ví dụ</th></tr>
<tr><td>So sánh</td><td>như, là, tựa, bao nhiêu… bấy nhiêu</td><td>Mặt trời xuống biển <i>như</i> hòn lửa</td></tr>
<tr><td>Nhân hóa</td><td>gán đặc điểm của người cho vật</td><td>Sóng đã cài then, đêm sập cửa</td></tr>
<tr><td>Ẩn dụ</td><td>gọi tên A bằng tên B (tương đồng)</td><td>Thấy một <i>mặt trời</i> trong lăng rất đỏ</td></tr>
<tr><td>Hoán dụ</td><td>gọi tên A bằng tên B (gần gũi)</td><td>Áo chàm đưa buổi phân li</td></tr>
<tr><td>Điệp ngữ</td><td>lặp lại từ, cụm từ</td><td>Thương em, thương em, thương em biết mấy</td></tr>
<tr><td>Nói quá</td><td>phóng đại</td><td>Lỗ mũi mười tám gánh lông</td></tr>
<tr><td>Liệt kê</td><td>kể ra nhiều sự vật liên tiếp</td><td>Tre, nứa, trúc, mai, vầu…</td></tr></table>
<div class="vd"><b>Cách trả lời tác dụng:</b> (1) Gọi tên biện pháp + chỉ ra từ ngữ → (2) Làm câu văn sinh động, gợi hình, gợi cảm → (3) Nhấn mạnh nội dung gì → (4) Thể hiện tình cảm gì của tác giả.</div>"""},
        {"ten": "Phương thức biểu đạt", "noi_dung": """
<ul>
<li><b>Tự sự:</b> kể chuỗi sự việc · <b>Miêu tả:</b> tái hiện hình ảnh</li>
<li><b>Biểu cảm:</b> bày tỏ cảm xúc · <b>Nghị luận:</b> dùng lí lẽ, dẫn chứng</li>
<li><b>Thuyết minh:</b> cung cấp tri thức · <b>Hành chính – công vụ:</b> đơn, giấy tờ</li>
</ul>"""},
        {"ten": "Thành phần biệt lập & Phép liên kết", "noi_dung": """
<p><b>Thành phần biệt lập:</b></p>
<ul>
<li>Tình thái: <i>chắc chắn, có lẽ, hình như…</i></li>
<li>Cảm thán: <i>ôi, trời ơi, chao ôi…</i></li>
<li>Gọi – đáp: <i>này, thưa ông, vâng…</i></li>
<li>Phụ chú: đặt giữa dấu gạch ngang, dấu phẩy, dấu ngoặc đơn.</li>
</ul>
<p><b>Phép liên kết câu:</b> lặp · thế · nối · đồng nghĩa/trái nghĩa · liên tưởng.</p>"""},
        {"ten": "Dàn ý đoạn nghị luận xã hội (200 chữ)", "noi_dung": """
<ol>
<li><b>Mở đoạn:</b> giới thiệu vấn đề.</li>
<li><b>Giải thích:</b> vấn đề là gì?</li>
<li><b>Bàn luận:</b> vì sao? biểu hiện? ý nghĩa? dẫn chứng thực tế.</li>
<li><b>Phản đề:</b> phê phán biểu hiện trái ngược.</li>
<li><b>Bài học:</b> nhận thức và hành động của bản thân.</li>
<li><b>Kết đoạn:</b> khẳng định lại vấn đề.</li>
</ol>
<div class="vd">✍️ Nhớ: viết đúng <b>một đoạn văn</b> (không xuống dòng), có câu chủ đề, dẫn chứng cụ thể, gần gũi.</div>"""},
        {"ten": "Dàn ý phân tích thơ / truyện", "noi_dung": """
<p><b>Phân tích thơ:</b> Mở bài (tác giả – tác phẩm – vấn đề) → Thân bài (nội dung từng khổ + nghệ thuật: hình ảnh, từ ngữ, biện pháp tu từ, nhịp điệu, thể thơ) → Đánh giá → Kết bài.</p>
<p><b>Phân tích truyện:</b> tóm tắt ngắn → phân tích nhân vật qua ngoại hình, lời nói, hành động, nội tâm → nghệ thuật (cốt truyện, tình huống, ngôi kể, chi tiết đặc sắc) → chủ đề, ý nghĩa.</p>"""},
        {"ten": "Tác phẩm tiêu biểu (tham khảo)", "noi_dung": """
<table class="bang"><tr><th>Tác phẩm</th><th>Tác giả</th><th>Năm</th></tr>
<tr><td>Đồng chí</td><td>Chính Hữu</td><td>1948</td></tr>
<tr><td>Bài thơ về tiểu đội xe không kính</td><td>Phạm Tiến Duật</td><td>1969</td></tr>
<tr><td>Đoàn thuyền đánh cá</td><td>Huy Cận</td><td>1958</td></tr>
<tr><td>Mùa xuân nho nhỏ</td><td>Thanh Hải</td><td>1980</td></tr>
<tr><td>Viếng lăng Bác</td><td>Viễn Phương</td><td>1976</td></tr>
<tr><td>Sang thu</td><td>Hữu Thỉnh</td><td>1977</td></tr>
<tr><td>Làng</td><td>Kim Lân</td><td>1948</td></tr>
<tr><td>Lặng lẽ Sa Pa</td><td>Nguyễn Thành Long</td><td>1970</td></tr>
<tr><td>Chiếc lược ngà</td><td>Nguyễn Quang Sáng</td><td>1966</td></tr>
<tr><td>Những ngôi sao xa xôi</td><td>Lê Minh Khuê</td><td>1971</td></tr></table>"""},
    ],
    "anh": [
        {"ten": "Các thì (Tenses)", "noi_dung": """
<table class="bang"><tr><th>Thì</th><th>Công thức (+)</th><th>Dấu hiệu</th></tr>
<tr><td>Hiện tại đơn</td><td>S + V(s/es)</td><td>always, usually, every day</td></tr>
<tr><td>Hiện tại tiếp diễn</td><td>S + am/is/are + V-ing</td><td>now, at the moment, Look!</td></tr>
<tr><td>Hiện tại hoàn thành</td><td>S + have/has + V3</td><td>for, since, already, yet, ever</td></tr>
<tr><td>Quá khứ đơn</td><td>S + V2/ed</td><td>yesterday, ago, last…</td></tr>
<tr><td>Quá khứ tiếp diễn</td><td>S + was/were + V-ing</td><td>at 8 pm yesterday, when, while</td></tr>
<tr><td>Tương lai đơn</td><td>S + will + V</td><td>tomorrow, next…, I think</td></tr></table>"""},
        {"ten": "Câu bị động (Passive voice)", "noi_dung": """
<p class="ct">S + be (chia theo thì) + V3/ed (+ by O)</p>
<ul>
<li>Hiện tại đơn: am/is/are + V3 · Quá khứ đơn: was/were + V3</li>
<li>Hiện tại hoàn thành: have/has been + V3 · Động từ khuyết thiếu: can/must/will + be + V3</li>
</ul>
<div class="vd">They <b>built</b> this bridge in 2000. → This bridge <b>was built</b> in 2000.</div>"""},
        {"ten": "Câu điều kiện (Conditionals)", "noi_dung": """
<table class="bang"><tr><th>Loại</th><th>If-clause</th><th>Main clause</th><th>Dùng khi</th></tr>
<tr><td>0</td><td>If + S + V(s)</td><td>S + V(s)</td><td>Sự thật hiển nhiên</td></tr>
<tr><td>1</td><td>If + S + V(s)</td><td>S + will + V</td><td>Có thể xảy ra ở hiện tại/tương lai</td></tr>
<tr><td>2</td><td>If + S + V2 (were)</td><td>S + would + V</td><td>Không có thật ở hiện tại</td></tr>
<tr><td>3</td><td>If + S + had + V3</td><td>S + would have + V3</td><td>Không có thật ở quá khứ</td></tr></table>
<div class="vd">Unless = If … not. &nbsp; If I <b>were</b> you, I <b>would</b> study harder.</div>"""},
        {"ten": "Câu ước (Wish)", "noi_dung": """
<ul>
<li>Hiện tại: <span class="ct">S + wish + S + V2/ed (were)</span> — I wish I <b>were</b> taller.</li>
<li>Quá khứ: <span class="ct">S + wish + S + had + V3</span> — I wish I <b>had studied</b> harder.</li>
<li>Tương lai: <span class="ct">S + wish + S + would + V</span> — I wish it <b>would</b> stop raining.</li>
</ul>"""},
        {"ten": "Mệnh đề quan hệ (Relative clauses)", "noi_dung": """
<ul>
<li><b>who</b>: chỉ người (chủ ngữ) · <b>whom</b>: chỉ người (tân ngữ)</li>
<li><b>which</b>: chỉ vật · <b>that</b>: người/vật (không dùng sau dấu phẩy, giới từ)</li>
<li><b>whose</b> + N: sở hữu · <b>where</b>: nơi chốn · <b>when</b>: thời gian</li>
</ul>
<div class="vd">The girl <b>who</b> sits next to me is Lan. · This is the house <b>where</b> I was born.</div>"""},
        {"ten": "Câu tường thuật (Reported speech)", "noi_dung": """
<ul>
<li>Lùi thì: hiện tại đơn → quá khứ đơn · hiện tại tiếp diễn → quá khứ tiếp diễn · will → would · can → could</li>
<li>Đổi trạng từ: now → then · today → that day · tomorrow → the next day · here → there · this → that</li>
<li>Câu hỏi Yes/No: <span class="ct">S + asked + if/whether + S + V(lùi thì)</span></li>
</ul>
<div class="vd">"I am tired," she said. → She said (that) she <b>was</b> tired.</div>"""},
        {"ten": "Phát âm -ed và -s/es", "noi_dung": """
<p><b>Đuôi -ed:</b></p>
<ul><li>/ɪd/: sau t, d — wanted, needed</li>
<li>/t/: sau p, k, f, s, ʃ, tʃ — stopped, looked, washed</li>
<li>/d/: các trường hợp còn lại — played, opened</li></ul>
<p><b>Đuôi -s/es:</b></p>
<ul><li>/s/: sau p, t, k, f, θ — books, stops</li>
<li>/ɪz/: sau s, z, ʃ, tʃ, dʒ — watches, boxes</li>
<li>/z/: các trường hợp còn lại — dogs, plays</li></ul>"""},
        {"ten": "V-ing hay To V?", "noi_dung": """
<ul>
<li><b>+ V-ing:</b> enjoy, avoid, mind, finish, suggest, practise, keep, be interested in, look forward to</li>
<li><b>+ to V:</b> want, decide, hope, plan, agree, refuse, learn, would like</li>
<li><b>+ V nguyên mẫu:</b> sau can, must, should, let, make, had better</li>
</ul>"""},
    ],
}

# ==============================================================
# 2. NGÂN HÀNG CÂU HỎI TRẮC NGHIỆM  (dap_an: 0=A, 1=B, 2=C, 3=D)
# ==============================================================
CAU_HOI = {
    "toan": {"ten": "Toán", "icon": "📐", "thoi_gian": 15, "cau": [
        {"hoi": "Giá trị của biểu thức √16 + √9 là:", "lua_chon": ["5", "7", "25", "12"], "dap_an": 1, "giai": "√16 = 4, √9 = 3 → 4 + 3 = 7."},
        {"hoi": "Điều kiện xác định của √(x − 3) là:", "lua_chon": ["x > 3", "x ≥ 3", "x ≤ 3", "x ≠ 3"], "dap_an": 1, "giai": "x − 3 ≥ 0 ⇔ x ≥ 3."},
        {"hoi": "Hệ phương trình { x + y = 5 ; x − y = 1 } có nghiệm là:", "lua_chon": ["(3; 2)", "(2; 3)", "(4; 1)", "(1; 4)"], "dap_an": 0, "giai": "Cộng hai phương trình: 2x = 6 → x = 3, y = 2."},
        {"hoi": "Phương trình x² − 5x + 6 = 0 có tập nghiệm là:", "lua_chon": ["{1; 6}", "{−2; −3}", "{2; 3}", "{−1; 6}"], "dap_an": 2, "giai": "Δ = 1 → x = (5 ± 1)/2 → x = 3; x = 2."},
        {"hoi": "Đồ thị hàm số y = ax² đi qua A(2; 8). Giá trị của a là:", "lua_chon": ["4", "2", "1/2", "16"], "dap_an": 1, "giai": "8 = a·4 → a = 2."},
        {"hoi": "Phương trình x² − 7x + 3 = 0 có hai nghiệm x₁, x₂. Tổng x₁ + x₂ bằng:", "lua_chon": ["3", "−7", "7", "−3"], "dap_an": 2, "giai": "Vi-ét: x₁ + x₂ = −b/a = 7."},
        {"hoi": "Hàm số y = (m − 2)x + 1 đồng biến trên ℝ khi:", "lua_chon": ["m < 2", "m > 2", "m = 2", "m ≠ 2"], "dap_an": 1, "giai": "a > 0 ⇔ m − 2 > 0 ⇔ m > 2."},
        {"hoi": "Tam giác ABC vuông tại A có AB = 3 cm, AC = 4 cm. BC bằng:", "lua_chon": ["5 cm", "7 cm", "6 cm", "25 cm"], "dap_an": 0, "giai": "BC² = 9 + 16 = 25 → BC = 5 cm."},
        {"hoi": "Góc nội tiếp chắn nửa đường tròn có số đo là:", "lua_chon": ["45°", "60°", "90°", "180°"], "dap_an": 2, "giai": "Góc nội tiếp chắn nửa đường tròn là góc vuông."},
        {"hoi": "Diện tích hình tròn bán kính R = 3 cm là:", "lua_chon": ["6π cm²", "9π cm²", "3π cm²", "12π cm²"], "dap_an": 1, "giai": "S = πR² = 9π cm²."},
        {"hoi": "Thể tích hình trụ có r = 2 cm, h = 5 cm là:", "lua_chon": ["10π cm³", "20π cm³", "40π cm³", "25π cm³"], "dap_an": 1, "giai": "V = πr²h = π·4·5 = 20π cm³."},
        {"hoi": "Đường thẳng y = 2x + 1 song song với đường thẳng:", "lua_chon": ["y = x + 1", "y = −2x + 1", "y = 2x − 3", "y = 2x + 1"], "dap_an": 2, "giai": "Song song ⇔ a = a', b ≠ b'."},
    ]},
    "van": {"ten": "Ngữ văn", "icon": "📖", "thoi_gian": 15, "cau": [
        {"hoi": "Tác giả của bài thơ \"Đồng chí\" là:", "lua_chon": ["Phạm Tiến Duật", "Chính Hữu", "Huy Cận", "Thanh Hải"], "dap_an": 1, "giai": "\"Đồng chí\" (1948) – Chính Hữu."},
        {"hoi": "\"Mặt trời xuống biển như hòn lửa\" sử dụng biện pháp tu từ:", "lua_chon": ["Ẩn dụ", "Hoán dụ", "So sánh", "Nhân hóa"], "dap_an": 2, "giai": "Có từ so sánh \"như\"."},
        {"hoi": "Anh thanh niên trong \"Lặng lẽ Sa Pa\" làm công việc gì?", "lua_chon": ["Kĩ sư nông nghiệp", "Họa sĩ", "Khí tượng kiêm vật lí địa cầu", "Lái xe"], "dap_an": 2, "giai": "Anh làm khí tượng kiêm vật lí địa cầu trên đỉnh Yên Sơn."},
        {"hoi": "Truyện \"Chiếc lược ngà\" là của nhà văn:", "lua_chon": ["Nguyễn Quang Sáng", "Kim Lân", "Nguyễn Thành Long", "Lê Minh Khuê"], "dap_an": 0, "giai": "Nguyễn Quang Sáng (1966)."},
        {"hoi": "\"Truyện Kiều\" được viết theo thể thơ:", "lua_chon": ["Song thất lục bát", "Lục bát", "Thất ngôn bát cú", "Tự do"], "dap_an": 1, "giai": "3254 câu thơ lục bát."},
        {"hoi": "Phương thức biểu đạt chính của văn nghị luận là:", "lua_chon": ["Tự sự", "Miêu tả", "Biểu cảm", "Nghị luận"], "dap_an": 3, "giai": "Dùng lí lẽ, dẫn chứng để thuyết phục."},
        {"hoi": "\"Trời ơi, chỉ còn có năm phút!\" chứa thành phần biệt lập:", "lua_chon": ["Tình thái", "Cảm thán", "Gọi – đáp", "Phụ chú"], "dap_an": 1, "giai": "\"Trời ơi\" bộc lộ cảm xúc."},
        {"hoi": "\"Mùa xuân nho nhỏ\" được Thanh Hải sáng tác năm:", "lua_chon": ["1965", "1975", "1980", "1986"], "dap_an": 2, "giai": "Tháng 11/1980."},
        {"hoi": "Từ \"đầu\" trong \"đầu súng trăng treo\" dùng theo nghĩa:", "lua_chon": ["Gốc", "Chuyển", "Không xác định", "Đồng âm"], "dap_an": 1, "giai": "Chỉ phần trên cùng của khẩu súng → nghĩa chuyển."},
        {"hoi": "Liên kết câu bằng cách lặp lại từ ngữ ở câu trước gọi là phép:", "lua_chon": ["Thế", "Nối", "Lặp", "Liên tưởng"], "dap_an": 2, "giai": "Phép lặp từ ngữ."},
        {"hoi": "\"Áo chàm đưa buổi phân li\" sử dụng biện pháp:", "lua_chon": ["Ẩn dụ", "Hoán dụ", "So sánh", "Điệp ngữ"], "dap_an": 1, "giai": "\"Áo chàm\" chỉ người Việt Bắc → hoán dụ."},
        {"hoi": "\"Có lẽ\" trong câu \"Có lẽ trời sắp mưa\" là thành phần:", "lua_chon": ["Tình thái", "Cảm thán", "Phụ chú", "Gọi – đáp"], "dap_an": 0, "giai": "Thể hiện mức độ tin cậy → tình thái."},
    ]},
    "anh": {"ten": "Tiếng Anh", "icon": "🇬🇧", "thoi_gian": 15, "cau": [
        {"hoi": "She ______ English for five years.", "lua_chon": ["learns", "has learned", "learned", "is learning"], "dap_an": 1, "giai": "\"for five years\" → hiện tại hoàn thành."},
        {"hoi": "If I ______ you, I would study harder.", "lua_chon": ["am", "was", "were", "be"], "dap_an": 2, "giai": "Điều kiện loại 2: If I were you."},
        {"hoi": "The house ______ in 1990.", "lua_chon": ["built", "was built", "is built", "has built"], "dap_an": 1, "giai": "Bị động quá khứ đơn: was + V3."},
        {"hoi": "Chọn từ có đuôi -ed phát âm khác:", "lua_chon": ["wanted", "needed", "played", "decided"], "dap_an": 2, "giai": "played /d/, còn lại /ɪd/."},
        {"hoi": "I wish I ______ a lot of money now.", "lua_chon": ["have", "had", "will have", "having"], "dap_an": 1, "giai": "Ước ở hiện tại: wish + V2."},
        {"hoi": "He is interested ______ playing football.", "lua_chon": ["on", "at", "in", "with"], "dap_an": 2, "giai": "be interested in + V-ing."},
        {"hoi": "The man ______ lives next door is a doctor.", "lua_chon": ["which", "who", "whom", "whose"], "dap_an": 1, "giai": "Chỉ người, làm chủ ngữ → who."},
        {"hoi": "\"Would you like some tea?\" – \"______\"", "lua_chon": ["Yes, I like.", "Yes, please.", "No, I wouldn't like.", "I don't."], "dap_an": 1, "giai": "Đáp lời mời: Yes, please / No, thanks."},
        {"hoi": "My mother suggested ______ to the park.", "lua_chon": ["go", "to go", "going", "went"], "dap_an": 2, "giai": "suggest + V-ing."},
        {"hoi": "Chọn từ có trọng âm khác:", "lua_chon": ["happy", "teacher", "begin", "student"], "dap_an": 2, "giai": "begin nhấn âm 2."},
        {"hoi": "She said she ______ tired.", "lua_chon": ["is", "was", "were", "be"], "dap_an": 1, "giai": "Tường thuật lùi thì: is → was."},
        {"hoi": "This is the village ______ I was born.", "lua_chon": ["which", "when", "where", "who"], "dap_an": 2, "giai": "Nơi chốn → where."},
    ]},
}

# ==============================================================
# 3. LUYỆN NGHE TIẾNG ANH (máy tính đọc bằng giọng tiếng Anh)
# ==============================================================
BAI_NGHE = [
    {"tieu_de": "Weekend plans", "muc_do": "Dễ",
     "doan": "Hi, I'm Tom. This weekend I am going to visit my grandparents in the countryside. "
             "We will go fishing on Saturday morning, and on Sunday I will help my grandmother in the garden. "
             "I will come back home on Sunday evening by bus.",
     "cau": [
        {"hoi": "Where is Tom going this weekend?", "lua_chon": ["To the beach", "To the countryside", "To the city", "To school"], "dap_an": 1},
        {"hoi": "What will they do on Saturday morning?", "lua_chon": ["Go fishing", "Go shopping", "Play football", "Watch TV"], "dap_an": 0},
        {"hoi": "How will Tom come back home?", "lua_chon": ["By car", "By train", "By bus", "On foot"], "dap_an": 2},
     ]},
    {"tieu_de": "At the library", "muc_do": "Trung bình",
     "doan": "Our school library opens from seven thirty in the morning to five o'clock in the afternoon. "
             "Students can borrow three books at a time for two weeks. "
             "Please keep quiet and do not bring food or drinks into the library.",
     "cau": [
        {"hoi": "What time does the library close?", "lua_chon": ["4 pm", "5 pm", "7:30 pm", "6 pm"], "dap_an": 1},
        {"hoi": "How many books can students borrow at a time?", "lua_chon": ["Two", "Three", "Four", "Five"], "dap_an": 1},
        {"hoi": "How long can students keep the books?", "lua_chon": ["One week", "Three days", "Two weeks", "One month"], "dap_an": 2},
     ]},
    {"tieu_de": "Protecting the environment", "muc_do": "Khó",
     "doan": "Plastic waste is one of the biggest problems for our planet. Every year, millions of tons of plastic end up in the ocean "
             "and harm sea animals. To help, we should bring our own bags when shopping, use reusable bottles, "
             "and recycle as much as possible. Small actions can make a big difference.",
     "cau": [
        {"hoi": "What is the main problem mentioned?", "lua_chon": ["Air pollution", "Plastic waste", "Noise", "Deforestation"], "dap_an": 1},
        {"hoi": "Where does a lot of plastic end up?", "lua_chon": ["In the forest", "In the sky", "In the ocean", "In the desert"], "dap_an": 2},
        {"hoi": "Which action is NOT suggested?", "lua_chon": ["Bring your own bags", "Use reusable bottles", "Recycle", "Burn plastic"], "dap_an": 3},
     ]},
]

NGHE_CHEP = [  # Nghe – chép chính tả
    "I usually get up at six o'clock.",
    "My favourite subject is English.",
    "We should save water and electricity.",
    "She has lived in Hanoi since two thousand twenty.",
    "If it rains tomorrow, we will stay at home.",
    "The Internet helps us learn many new things.",
]

# ==============================================================
# 4. LUYỆN NÓI TIẾNG ANH (nhận diện giọng nói của bạn)
# ==============================================================
BAI_NOI = {
    "Từ vựng": ["environment", "technology", "comfortable", "vegetable", "temperature",
                "education", "volunteer", "pollution", "celebrate", "traditional"],
    "Câu giao tiếp": ["How are you today?", "Nice to meet you.", "Could you help me, please?",
                      "What do you do in your free time?", "I'm sorry, I'm late.",
                      "Thank you very much for your help.", "Can you speak more slowly, please?"],
    "Giới thiệu bản thân": ["My name is Lan and I am fifteen years old.",
                            "I am a student at Nguyen Du secondary school.",
                            "In my free time, I like reading books and playing badminton.",
                            "I want to become a doctor in the future.",
                            "I live with my parents and my younger brother."],
    "Chủ đề thi": ["We should plant more trees to protect the environment.",
                   "Learning English is very important for our future.",
                   "Tet is the most important festival in Vietnam.",
                   "Social media has both advantages and disadvantages."],
}

# ==============================================================
# 5. TRỢ LÝ AI HỖ TRỢ HỌC TẬP
# ==============================================================
try:
    import anthropic
except ImportError:
    anthropic = None

HUONG_DAN_AI = """Bạn là "Thầy Cô AI" - trợ lý học tập thân thiện giúp học sinh lớp 9 Việt Nam ôn thi tuyển sinh vào lớp 10, gồm ba môn Toán, Ngữ văn và Tiếng Anh (theo chương trình giáo dục phổ thông hiện hành).
Cách trả lời:
- Luôn trả lời bằng tiếng Việt, giọng gần gũi, khích lệ; xưng "mình", gọi học sinh là "bạn".
- Toán: giải từng bước rõ ràng, nêu công thức dùng ở mỗi bước, kết luận đáp số; viết ký hiệu toán dễ đọc (x², √, ≥, Δ...), không dùng LaTeX.
- Ngữ văn: hướng dẫn cách làm, lập dàn ý, gợi ý ý chính và dẫn chứng; nếu bạn ấy nhờ viết cả bài thì có thể viết mẫu nhưng nhắc bạn tự viết lại bằng lời của mình.
- Tiếng Anh: giải thích ngữ pháp kèm công thức, ví dụ và nghĩa tiếng Việt; khi sửa câu thì chỉ rõ lỗi sai.
- Trình bày ngắn gọn, dùng gạch đầu dòng và **in đậm** ý quan trọng. Cuối câu trả lời có thể gợi ý một câu luyện tập tương tự.
- Nếu câu hỏi không liên quan đến học tập, nhẹ nhàng hướng bạn ấy quay lại việc ôn thi."""

_client_ai = None


def co_ai():
    """Kiểm tra đã đủ điều kiện dùng AI thật chưa."""
    if anthropic is None:
        return False, "Chưa cài thư viện anthropic (chạy: pip install anthropic)"
    if not (API_KEY or os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")):
        return False, "Chưa có khóa API (điền API_KEY trong file hoặc đặt biến ANTHROPIC_API_KEY)"
    return True, "Đã kết nối AI"


def lay_client():
    global _client_ai
    if _client_ai is None:
        _client_ai = anthropic.Anthropic(api_key=API_KEY) if API_KEY else anthropic.Anthropic()
    return _client_ai


def hoi_ai(tin_nhan):
    """Gửi lịch sử hội thoại tới Claude và nhận câu trả lời."""
    client = lay_client()
    try:
        # Bật dự phòng phía máy chủ: nếu mô hình chính từ chối, API tự chuyển sang mô hình khác
        resp = client.beta.messages.create(
            model=MODEL_AI, max_tokens=16000, system=HUONG_DAN_AI, messages=tin_nhan,
            output_config={"effort": "low"},
            betas=["server-side-fallback-2026-07-01"], fallbacks="default",
        )
    except TypeError:
        # Thư viện anthropic bản cũ chưa hỗ trợ các tham số trên -> gọi cơ bản
        resp = client.messages.create(model=MODEL_AI, max_tokens=16000,
                                      system=HUONG_DAN_AI, messages=tin_nhan)
    if resp.stop_reason == "refusal":
        return "Xin lỗi, mình không thể trả lời câu này. Bạn thử hỏi câu khác về Toán, Văn hoặc Anh nhé! 🙏"
    tra_loi = "".join(b.text for b in resp.content if b.type == "text").strip()
    if resp.stop_reason == "max_tokens":
        tra_loi += "\n\n_(Câu trả lời dài quá nên bị cắt bớt, bạn hỏi tiếp \"tiếp tục\" nhé.)_"
    return tra_loi or "Mình chưa nghĩ ra câu trả lời, bạn hỏi lại theo cách khác nhé!"


TU_BO_QUA = set("""là của và có cho các những một được trong với thì mà này đó em mình bạn tôi ạ ơi
gì nào sao thế nào làm ra về khi hay hoặc không giúp hỏi cách bài câu""".split())


def html_sang_chu(h):
    h = re.sub(r"<li>", "\n- ", h)
    h = re.sub(r"</(p|tr|ul|ol|div)>|<br>", "\n", h)
    h = re.sub(r"</t[dh]>", " | ", h)
    h = re.sub(r"<b>|</b>", "**", h)
    h = re.sub(r"<[^>]+>", "", h)
    h = html.unescape(h)
    return re.sub(r"\n\s*\n+", "\n", h).strip()


def tra_loi_offline(cau):
    """Chế độ offline: tìm chuyên đề lý thuyết khớp nhất với câu hỏi."""
    q = cau.lower()
    if len(q) < 30 and any(x in q for x in ("xin chào", "chào", "hello", "hi ")):
        return ("Chào bạn! 👋 Mình là trợ lý ôn thi vào 10. Bạn có thể hỏi về **Toán, Ngữ văn, Tiếng Anh**, "
                "ví dụ: *\"Vi-ét là gì?\"*, *\"câu bị động\"*, *\"biện pháp tu từ\"*.")
    tu = {t for t in re.findall(r"\w+", q) if t not in TU_BO_QUA and len(t) > 1}
    ket_qua = []
    for mon, ds in LY_THUYET.items():
        for cd in ds:
            ten = cd["ten"].lower()
            van = ten + " " + html_sang_chu(cd["noi_dung"]).lower()
            diem = sum(3 if t in ten else 1 for t in tu if t in van)
            ket_qua.append((diem, mon, cd))
    ket_qua.sort(key=lambda x: -x[0])
    if not ket_qua or ket_qua[0][0] < 2:
        return ("🤔 Ở chế độ offline mình chỉ tra cứu được phần **Lý thuyết** có sẵn và chưa tìm thấy nội dung phù hợp.\n"
                "Bạn thử dùng từ khóa như: *căn bậc hai, Vi-ét, hệ phương trình, đường tròn, tu từ, nghị luận, "
                "bị động, câu điều kiện, câu ước...*\n\n"
                "💡 Muốn hỏi **bất kỳ câu nào** (giải bài, sửa bài văn...), hãy bật AI: `pip install anthropic` và điền khóa API.")
    _, mon, cd = ket_qua[0]
    ten_mon = {"toan": "Toán", "van": "Ngữ văn", "anh": "Tiếng Anh"}[mon]
    goi_y = [k[2]["ten"] for k in ket_qua[1:3] if k[0] >= 2]
    tra_loi = f"📚 **{cd['ten']}** ({ten_mon})\n{html_sang_chu(cd['noi_dung'])}"
    if goi_y:
        tra_loi += "\n\n🔎 Có thể bạn cũng cần: " + ", ".join(goi_y)
    return tra_loi + "\n\n_(Chế độ offline - bật AI để được giải thích chi tiết hơn)_"


def xu_ly_chat(du_lieu):
    tin = []
    for m in du_lieu.get("messages", [])[-20:]:
        if m.get("role") in ("user", "assistant") and isinstance(m.get("content"), str) and m["content"].strip():
            tin.append({"role": m["role"], "content": m["content"][:4000]})
    while tin and tin[0]["role"] != "user":
        tin.pop(0)
    if not tin or tin[-1]["role"] != "user":
        return {"reply": "Bạn hãy nhập câu hỏi nhé!", "che_do": "offline"}
    duoc, ly_do = co_ai()
    if duoc:
        try:
            return {"reply": hoi_ai(tin), "che_do": "ai"}
        except anthropic.AuthenticationError:
            loi = "Khóa API không hợp lệ, hãy kiểm tra lại API_KEY."
        except anthropic.PermissionDeniedError:
            loi = "Khóa API không có quyền dùng mô hình này."
        except anthropic.RateLimitError:
            loi = "AI đang quá tải hoặc hết hạn mức, thử lại sau ít phút."
        except anthropic.APIConnectionError:
            loi = "Không kết nối được tới máy chủ AI (kiểm tra Internet)."
        except anthropic.APIStatusError as e:
            loi = f"Máy chủ AI báo lỗi {e.status_code}."
        except Exception as e:  # lỗi khác (vd: thiếu thông tin xác thực)
            loi = f"Lỗi AI: {e}"
        return {"reply": f"⚠️ {loi}\n\n" + tra_loi_offline(tin[-1]["content"]), "che_do": "offline"}
    return {"reply": tra_loi_offline(tin[-1]["content"]), "che_do": "offline", "ly_do": ly_do}


# ==============================================================
# 6. GIAO DIỆN WEB
# ==============================================================
HTML = r"""<!DOCTYPE html>
<html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ôn Thi Vào 10</title>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--p:#6366f1;--p2:#8b5cf6;--hong:#ec4899;--xanh:#10b981;--do:#ef4444;--vang:#f59e0b;
--nen:#f5f7ff;--the:#fff;--chu:#1e293b;--mo:#64748b;--vien:#e2e8f0}
*{box-sizing:border-box}
body{margin:0;font-family:'Be Vietnam Pro',Segoe UI,Arial,sans-serif;background:var(--nen);color:var(--chu)}
a{color:inherit}
/* ---------- thanh điều hướng ---------- */
nav{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.95);backdrop-filter:blur(12px);
border-bottom:1px solid var(--vien)}
.nav{max-width:1300px;margin:auto;display:flex;align-items:center;gap:3px;padding:8px 12px;flex-wrap:nowrap;overflow-x:auto}
.logo{font-weight:800;font-size:18px;margin-right:4px;white-space:nowrap;
background:linear-gradient(90deg,var(--p),var(--hong));-webkit-background-clip:text;color:transparent}
.tab{border:0;background:none;padding:6px 10px;border-radius:999px;font-weight:600;font-size:13px;font-family:inherit;
color:var(--mo);cursor:pointer;white-space:nowrap;transition:.2s}
.tab:hover{background:#eef2ff;color:var(--p)}
.tab.on{background:linear-gradient(135deg,var(--p),var(--p2));color:#fff;box-shadow:0 4px 12px rgba(99,102,241,.35)}
/* ---------- chung ---------- */
.wrap{max-width:1100px;margin:auto;padding:24px 16px 40px}
.trang{display:none;animation:hien .45s ease}.trang.on{display:block}
@keyframes hien{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
h2.tt{font-size:28px;margin:0 0 6px}.phu{color:var(--mo);margin:0 0 22px}
.the{background:var(--the);border-radius:20px;padding:22px;box-shadow:0 6px 24px rgba(30,41,59,.06);border:1px solid var(--vien)}
.luoi{display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.nut{border:0;border-radius:12px;padding:12px 22px;font-weight:700;font-size:15px;font-family:inherit;cursor:pointer;
color:#fff;background:linear-gradient(135deg,var(--p),var(--p2));transition:.2s;box-shadow:0 4px 14px rgba(99,102,241,.3)}
.nut:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(99,102,241,.4)}
.nut:disabled{opacity:.5;cursor:not-allowed;transform:none}
.nut.phu2{background:#fff;color:var(--p);border:2px solid var(--p);box-shadow:none}
.nut.xanh{background:linear-gradient(135deg,#10b981,#059669);box-shadow:0 4px 14px rgba(16,185,129,.3)}
.nut.hong{background:linear-gradient(135deg,#ec4899,#f43f5e);box-shadow:0 4px 14px rgba(236,72,153,.3)}
.chip{display:inline-block;padding:4px 12px;border-radius:999px;font-size:12px;font-weight:700;background:#eef2ff;color:var(--p)}
/* ---------- hero ---------- */
.hero{position:relative;overflow:hidden;border-radius:28px;padding:48px 32px;color:#fff;
background:linear-gradient(135deg,#6366f1 0%,#8b5cf6 50%,#ec4899 100%)}
.hero h1{font-size:clamp(28px,5vw,46px);margin:0 0 10px;line-height:1.15}
.hero p{font-size:17px;opacity:.92;max-width:560px;margin:0 0 24px}
.hero .nut{background:#fff;color:var(--p)}
.bong{position:absolute;border-radius:50%;background:rgba(255,255,255,.14);animation:troi 8s ease-in-out infinite}
@keyframes troi{50%{transform:translateY(-22px) scale(1.06)}}
.dem{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}
.dem div{background:rgba(255,255,255,.18);border-radius:16px;padding:12px 16px;text-align:center;min-width:76px}
.dem b{display:block;font-size:28px}.dem span{font-size:12px;opacity:.85}
.mon{cursor:pointer;transition:.25s;position:relative;overflow:hidden}
.mon:hover{transform:translateY(-6px);box-shadow:0 14px 32px rgba(99,102,241,.18)}
.mon .ic{width:64px;height:64px;border-radius:18px;display:grid;place-items:center;font-size:34px;margin-bottom:12px}
.mon h3{margin:0 0 6px;font-size:20px}.mon p{margin:0;color:var(--mo);font-size:14px}
.thongke{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin:22px 0}
.thongke .the{text-align:center;padding:18px}.thongke b{font-size:30px;display:block;color:var(--p)}
/* ---------- lý thuyết ---------- */
.monTab{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:18px}
.acc{margin-bottom:12px;padding:0;overflow:hidden}
.acc>button{width:100%;text-align:left;border:0;background:none;padding:18px 22px;font-weight:700;font-size:17px;font-family:inherit;
cursor:pointer;display:flex;align-items:center;gap:12px;color:var(--chu)}
.acc>button .so{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;color:#fff;font-size:14px;
background:linear-gradient(135deg,var(--p),var(--p2));flex:none}
.acc>button .mt{margin-left:auto;transition:.3s;color:var(--mo)}
.acc.mo>button .mt{transform:rotate(180deg)}
.acc .nd{max-height:0;overflow:hidden;transition:max-height .4s ease;padding:0 22px}
.acc.mo .nd{max-height:1500px;padding-bottom:18px}
.nd li{margin:7px 0;line-height:1.6}.nd p{line-height:1.6}
.ct{background:#eef2ff;color:#4338ca;padding:2px 8px;border-radius:6px;font-weight:600;display:inline-block}
.vd{background:linear-gradient(135deg,#fef3c7,#fde68a40);border-left:4px solid var(--vang);padding:12px 14px;border-radius:10px;margin-top:10px}
.bang{width:100%;border-collapse:collapse;margin:8px 0;font-size:14px}
.bang th{background:#eef2ff;color:#4338ca;text-align:left}.bang th,.bang td{padding:9px 10px;border-bottom:1px solid var(--vien)}
.timkiem{width:100%;padding:13px 18px;border-radius:14px;border:2px solid var(--vien);font-size:15px;font-family:inherit;margin-bottom:16px;outline:0}
.timkiem:focus{border-color:var(--p)}
/* ---------- luyện đề ---------- */
.bar{position:sticky;top:62px;z-index:10;background:var(--the);border-radius:16px;padding:14px 18px;margin-bottom:16px;
box-shadow:0 6px 18px rgba(0,0,0,.06);display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.tien{flex:1;min-width:120px;height:10px;background:#e0e7ff;border-radius:99px;overflow:hidden}
.tien div{height:100%;width:0;background:linear-gradient(90deg,var(--p),var(--hong));transition:.3s}
.gio{font-weight:800;font-size:20px;color:var(--do)}
.q{margin-bottom:14px}.q h4{margin:0 0 12px;font-size:16px;line-height:1.5}
.opt{display:flex;align-items:center;gap:10px;padding:12px 14px;border:2px solid var(--vien);border-radius:12px;margin:8px 0;cursor:pointer;transition:.15s}
.opt:hover{border-color:#a5b4fc;background:#f5f7ff}
.opt input{display:none}
.opt .kt{width:30px;height:30px;border-radius:9px;background:#eef2ff;color:var(--p);display:grid;place-items:center;font-weight:800;flex:none}
.opt.chon{border-color:var(--p);background:#eef2ff}.opt.chon .kt{background:var(--p);color:#fff}
.opt.dung{border-color:var(--xanh);background:#d1fae5}.opt.dung .kt{background:var(--xanh);color:#fff}
.opt.sai{border-color:var(--do);background:#fee2e2}.opt.sai .kt{background:var(--do);color:#fff}
.giai{margin-top:10px;padding:10px 14px;background:#fef9c3;border-radius:10px;font-size:14px}
.vong{width:170px;height:170px;border-radius:50%;margin:10px auto;display:grid;place-items:center}
.vong div{width:136px;height:136px;border-radius:50%;background:#fff;display:grid;place-items:center;font-size:40px;font-weight:800;color:var(--p)}
/* ---------- nghe & nói ---------- */
.loa{width:120px;height:120px;border-radius:50%;border:0;cursor:pointer;font-size:46px;color:#fff;margin:10px auto;display:grid;place-items:center;
background:linear-gradient(135deg,var(--p),var(--hong));box-shadow:0 10px 30px rgba(236,72,153,.4);transition:.2s}
.loa:hover{transform:scale(1.06)}
.loa.dang{animation:dap 1s infinite}
@keyframes dap{0%{box-shadow:0 0 0 0 rgba(236,72,153,.55)}100%{box-shadow:0 0 0 28px rgba(236,72,153,0)}}
.song{display:flex;gap:4px;justify-content:center;height:34px;align-items:center;margin:6px 0}
.song i{width:5px;background:var(--p);border-radius:3px;height:6px}
.song.chay i{animation:nhay .8s ease-in-out infinite}
.song i:nth-child(2){animation-delay:.1s}.song i:nth-child(3){animation-delay:.2s}.song i:nth-child(4){animation-delay:.3s}
.song i:nth-child(5){animation-delay:.4s}.song i:nth-child(6){animation-delay:.5s}.song i:nth-child(7){animation-delay:.6s}
@keyframes nhay{50%{height:32px}}
.dk{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;align-items:center;margin:8px 0}
select,input[type=text],input[type=password],input[type=email]{padding:11px 14px;border-radius:12px;border:2px solid var(--vien);font-size:15px;font-family:inherit;outline:0;background:#fff}
input[type=text],input[type=password],input[type=email]{width:100%}
input[type=text]:focus,input[type=password]:focus,input[type=email]:focus,select:focus{border-color:var(--p)}
.cauNoi{font-size:clamp(20px,3.4vw,30px);font-weight:700;text-align:center;margin:18px 0;line-height:1.4}
.mic{width:110px;height:110px;border-radius:50%;border:0;font-size:44px;cursor:pointer;color:#fff;margin:auto;display:grid;place-items:center;
background:linear-gradient(135deg,#10b981,#059669);box-shadow:0 10px 26px rgba(16,185,129,.4);transition:.2s}
.mic.ghi{background:linear-gradient(135deg,#ef4444,#f43f5e);animation:dapDo 1s infinite}
@keyframes dapDo{0%{box-shadow:0 0 0 0 rgba(239,68,68,.55)}100%{box-shadow:0 0 0 30px rgba(239,68,68,0)}}
.tu{display:inline-block;padding:4px 10px;margin:3px;border-radius:8px;font-weight:600}
.tu.d{background:#d1fae5;color:#047857}.tu.s{background:#fee2e2;color:#b91c1c;text-decoration:underline wavy}
.bao{padding:12px 16px;border-radius:12px;background:#fff7ed;color:#9a3412;border:1px solid #fed7aa;margin-bottom:14px}
.an{display:none!important}
footer{text-align:center;color:var(--mo);padding:24px;font-size:13px}
#phao{position:fixed;inset:0;pointer-events:none;z-index:99}
/* ---------- đăng nhập / tài khoản góc phải ---------- */
.auth-khung{display:flex;align-items:center;gap:4px;margin-left:auto;flex-shrink:0}
.user-pill{display:flex;align-items:center;gap:4px;background:#eef2ff;padding:4px 8px;border-radius:999px;font-weight:700;font-size:12px;color:var(--p);white-space:nowrap}
/* Modal đăng nhập */
.modal-overlay{position:fixed;inset:0;background:rgba(15,23,42,.6);backdrop-filter:blur(6px);z-index:100;display:grid;place-items:center;animation:hien .25s ease}
.modal-box{background:#fff;border-radius:24px;padding:32px;width:100%;max-width:420px;box-shadow:0 25px 50px rgba(0,0,0,.25);position:relative}
.modal-box h2{margin-top:0;font-size:24px;margin-bottom:8px}
.form-nhom{margin-bottom:16px}
.form-nhom label{display:block;font-weight:600;font-size:13.5px;margin-bottom:6px;color:var(--chu)}
.form-loi{color:var(--do);font-size:13px;margin-top:6px;min-height:18px}
.form-chuyen{text-align:center;margin-top:16px;font-size:14px;color:var(--mo)}
.form-chuyen a{color:var(--p);font-weight:700;cursor:pointer;text-decoration:none}
.form-chuyen a:hover{text-decoration:underline}
/* ---------- trợ lý AI ---------- */
#chatNut{position:fixed;right:22px;bottom:22px;z-index:90;border:0;cursor:pointer;color:#fff;font-family:inherit;
display:flex;align-items:center;gap:8px;padding:14px 20px;border-radius:999px;font-size:26px;
background:linear-gradient(135deg,#6366f1,#ec4899);box-shadow:0 10px 30px rgba(99,102,241,.45);transition:.25s;animation:noi 2.5s ease-in-out infinite}
#chatNut span{font-size:15px;font-weight:700}
#chatNut:hover{transform:scale(1.07)}
@keyframes noi{50%{transform:translateY(-6px)}}
#chatHop{position:fixed;right:22px;bottom:22px;z-index:95;width:400px;max-width:calc(100vw - 32px);height:600px;max-height:calc(100vh - 44px);
background:#fff;border-radius:24px;box-shadow:0 20px 60px rgba(30,41,59,.3);display:flex;flex-direction:column;overflow:hidden;animation:hien .3s ease}
.chatDau{display:flex;align-items:center;gap:12px;padding:14px 16px;color:#fff;background:linear-gradient(135deg,#6366f1,#8b5cf6,#ec4899)}
.chatDau .av{width:44px;height:44px;border-radius:14px;background:rgba(255,255,255,.22);display:grid;place-items:center;font-size:24px}
.chatDau small{display:block;opacity:.9;font-size:12px}
.chatDau button{margin-left:auto;border:0;background:rgba(255,255,255,.2);color:#fff;width:34px;height:34px;border-radius:10px;cursor:pointer;font-size:16px}
#chatThan{flex:1;overflow-y:auto;padding:16px;background:#f5f7ff;display:flex;flex-direction:column;gap:10px}
.tin{max-width:86%;padding:11px 14px;border-radius:18px;line-height:1.6;font-size:14.5px;word-wrap:break-word;animation:hien .25s ease}
.tin.user{align-self:flex-end;color:#fff;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-bottom-right-radius:6px}
.tin.bot{align-self:flex-start;background:#fff;border:1px solid var(--vien);border-bottom-left-radius:6px}
.tin li{margin:3px 0 3px 18px}.tin pre{background:#1e293b;color:#e2e8f0;padding:10px;border-radius:10px;overflow-x:auto;white-space:pre-wrap}
.tin code{background:#eef2ff;color:#4338ca;padding:1px 6px;border-radius:5px}
.tin .h{display:block;color:var(--p);margin-top:4px}
.go{display:inline-flex;gap:4px}.go i{width:8px;height:8px;border-radius:50%;background:#a5b4fc;animation:nhay2 1s infinite}
.go i:nth-child(2){animation-delay:.15s}.go i:nth-child(3){animation-delay:.3s}
@keyframes nhay2{50%{transform:translateY(-6px);background:var(--p)}}
#chatGoiY{display:flex;gap:6px;padding:8px 12px 0;overflow-x:auto;background:#fff}
#chatGoiY button{flex:none;border:1px solid #c7d2fe;background:#eef2ff;color:var(--p);border-radius:999px;padding:6px 12px;font:600 12.5px 'Be Vietnam Pro',sans-serif;cursor:pointer}
#chatForm{display:flex;gap:8px;padding:12px;background:#fff;border-top:1px solid var(--vien)}
#chatNhap{flex:1;resize:none;border:2px solid var(--vien);border-radius:14px;padding:10px 12px;font-size:14.5px;font-family:inherit;outline:0;max-height:110px}
#chatNhap:focus{border-color:var(--p)}
#chatForm button{border:0;width:46px;border-radius:14px;color:#fff;font-size:18px;cursor:pointer;background:linear-gradient(135deg,#6366f1,#ec4899)}
.nut.nho{padding:5px 10px;font-size:12px;margin-top:0}
@media(max-width:950px){.auth-khung{margin-left:0;width:100%;justify-content:flex-end;margin-top:4px}}
@media(max-width:600px){#chatHop{right:0;bottom:0;width:100vw;max-width:100vw;height:100vh;max-height:100vh;border-radius:0}#chatNut span{display:none}}
@media(max-width:600px){.hero{padding:34px 20px}.bar{top:58px}}
</style></head><body>
<canvas id="phao"></canvas>
<nav><div class="nav">
  <span class="logo">🎓 ÔnThi10</span>
  <button class="tab on" data-t="home">🏠 Trang chủ</button>
  <button class="tab" data-t="lythuyet">📚 Lý thuyết</button>
  <button class="tab" data-t="luyende">📝 Luyện đề</button>
  <button class="tab" data-t="nghe">🎧 Luyện nghe</button>
  <button class="tab" data-t="noi">🎤 Luyện nói</button>
  <button class="tab" onclick="moChat()">🤖 Trợ lý AI</button>
  <div class="auth-khung" id="vungAuth"></div>
</div></nav>

<div class="wrap">
<!-- ===================== TRANG CHỦ ===================== -->
<section class="trang on" id="home">
  <div class="hero">
    <span class="bong" style="width:220px;height:220px;right:-40px;top:-50px"></span>
    <span class="bong" style="width:120px;height:120px;right:160px;bottom:-30px;animation-delay:2s"></span>
    <span class="bong" style="width:70px;height:70px;right:60px;bottom:40px;animation-delay:4s"></span>
    <h1>Chinh phục kỳ thi<br>vào lớp 10 🚀</h1>
    <p>Học lý thuyết trọng tâm, luyện đề có chấm điểm, luyện nghe và nói tiếng Anh. Tất cả trong một trang web!</p>
    <button class="nut" onclick="moTab('luyende')">Bắt đầu luyện đề →</button>
    <div class="dem" id="demNguoc"></div>
  </div>

  <div class="thongke">
    <div class="the"><b id="tkBai">0</b>Bài đã làm</div>
    <div class="the"><b id="tkTB">0</b>Điểm trung bình</div>
    <div class="the"><b id="tkCao">0</b>Điểm cao nhất</div>
    <div class="the"><b id="tkNoi">0</b>Câu đã luyện nói</div>
  </div>

  <h2 class="tt">Khám phá</h2><p class="phu">Chọn một mục để bắt đầu ôn tập</p>
  <div class="luoi">
    <div class="the mon" onclick="moTab('lythuyet','toan')"><div class="ic" style="background:#e0e7ff">📐</div><h3>Toán</h3><p>Căn thức, hàm số, phương trình bậc hai, Vi-ét, hình học</p></div>
    <div class="the mon" onclick="moTab('lythuyet','van')"><div class="ic" style="background:#fce7f3">📖</div><h3>Ngữ văn</h3><p>Biện pháp tu từ, đọc hiểu, dàn ý nghị luận</p></div>
    <div class="the mon" onclick="moTab('lythuyet','anh')"><div class="ic" style="background:#d1fae5">🇬🇧</div><h3>Tiếng Anh</h3><p>Ngữ pháp trọng tâm, phát âm, cấu trúc câu</p></div>
    <div class="the mon" onclick="moTab('nghe')"><div class="ic" style="background:#fef3c7">🎧</div><h3>Luyện nghe</h3><p>Nghe đoạn hội thoại, trả lời câu hỏi, chép chính tả</p></div>
    <div class="the mon" onclick="moTab('noi')"><div class="ic" style="background:#ffe4e6">🎤</div><h3>Luyện nói</h3><p>Đọc to, máy chấm phát âm từng từ</p></div>
    <div class="the mon" onclick="moChat()"><div class="ic" style="background:#ede9fe">🤖</div><h3>Trợ lý AI</h3><p>Hỏi bài, giải toán từng bước, sửa văn, giải thích ngữ pháp</p></div>
  </div>

  <div class="the" style="margin-top:22px"><h3 style="margin-top:0">📊 Lịch sử làm bài</h3><div id="lichSu" style="color:var(--mo)">Chưa có bài làm nào.</div></div>
</section>

<!-- ===================== LÝ THUYẾT ===================== -->
<section class="trang" id="lythuyet">
  <h2 class="tt">📚 Lý thuyết trọng tâm</h2><p class="phu">Bấm vào từng chuyên đề để xem chi tiết</p>
  <div class="monTab" id="ltTab"></div>
  <input class="timkiem" id="ltTim" placeholder="🔍 Tìm chuyên đề... (vd: Vi-ét, bị động, tu từ)">
  <div id="ltDs"></div>
</section>

<!-- ===================== LUYỆN ĐỀ ===================== -->
<section class="trang" id="luyende">
  <div id="deChon">
    <h2 class="tt">📝 Luyện đề trắc nghiệm</h2><p class="phu">Câu hỏi được trộn ngẫu nhiên mỗi lần làm. Hết giờ sẽ tự nộp bài.</p>
    <div class="luoi" id="dsMon"></div>
  </div>
  <div id="deLam" class="an">
    <div class="bar"><b id="tenMon"></b><div class="tien"><div id="tienDo"></div></div><span id="daLam" class="chip"></span><span class="gio" id="gio"></span></div>
    <div id="dsCau"></div>
    <div style="text-align:center;margin-top:10px"><button class="nut" onclick="nopBai()">📮 Nộp bài</button></div>
  </div>
  <div id="deKq" class="an">
    <div class="the" style="text-align:center">
      <h2 id="kqMon" style="margin:0"></h2>
      <div class="vong" id="kqVong"><div id="kqDiem"></div></div>
      <p id="kqNx" style="font-size:18px;font-weight:600"></p>
      <div class="dk"><button class="nut" onclick="batDau(monHT)">🔁 Làm lại</button><button class="nut phu2" onclick="veChonDe()">📋 Chọn môn khác</button></div>
    </div>
    <h3>Đáp án & lời giải</h3><div id="kqCt"></div>
  </div>
</section>

<!-- ===================== LUYỆN NGHE ===================== -->
<section class="trang" id="nghe">
  <h2 class="tt">🎧 Luyện nghe tiếng Anh</h2><p class="phu">Bấm loa để nghe. Có thể chỉnh tốc độ và nghe lại nhiều lần.</p>
  <div class="monTab">
    <button class="nut" id="ngheTab1" onclick="cheDoNghe(1)">💬 Nghe & trả lời</button>
    <button class="nut phu2" id="ngheTab2" onclick="cheDoNghe(2)">✍️ Nghe & chép chính tả</button>
  </div>
  <div class="dk the" style="padding:12px;margin-bottom:16px">
    <label>Tốc độ: <select id="tocDo"><option value="0.7">🐢 Chậm</option><option value="0.9" selected>🙂 Vừa</option><option value="1.1">🐇 Nhanh</option></select></label>
    <label>Giọng: <select id="giong"></select></label>
  </div>

  <div id="nghe1">
    <div class="dk" id="dsBaiNghe" style="justify-content:flex-start"></div>
    <div class="the" style="text-align:center;margin-top:10px">
      <h3 id="ngheTen" style="margin:0"></h3><span class="chip" id="ngheMuc"></span>
      <button class="loa" id="loa1" onclick="docBai()">🔊</button>
      <div class="song" id="song1"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
      <div class="dk"><button class="nut phu2" onclick="dungDoc()">⏹ Dừng</button>
      <button class="nut phu2" onclick="hienLoi()">📄 Hiện / ẩn lời bài nghe</button></div>
      <p id="loiBai" class="an" style="text-align:left;background:#f5f7ff;padding:14px;border-radius:12px;line-height:1.7"></p>
    </div>
    <div id="ngheCau" style="margin-top:16px"></div>
    <div style="text-align:center"><button class="nut" onclick="chamNghe()">✅ Kiểm tra đáp án</button></div>
    <p id="ngheKq" style="text-align:center;font-size:20px;font-weight:700"></p>
  </div>

  <div id="nghe2" class="an">
    <div class="the" style="text-align:center">
      <span class="chip" id="chepSo"></span>
      <button class="loa" id="loa2" onclick="docChep()">🔊</button>
      <div class="song" id="song2"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
      <input type="text" id="chepNhap" placeholder="Gõ lại câu bạn nghe được rồi nhấn Enter..." autocomplete="off">
      <div class="dk" style="margin-top:14px"><button class="nut" onclick="kiemTraChep()">✅ Kiểm tra</button>
      <button class="nut phu2" onclick="cauChep(1)">Câu tiếp ➜</button></div>
      <div id="chepKq" style="margin-top:12px"></div>
    </div>
  </div>
</section>

<!-- ===================== LUYỆN NÓI ===================== -->
<section class="trang" id="noi">
  <h2 class="tt">🎤 Luyện nói tiếng Anh</h2><p class="phu">Nghe mẫu → bấm micro → đọc to. Máy sẽ chấm điểm và tô màu từng từ.</p>
  <div class="bao an" id="noiBao">⚠️ Trình duyệt này chưa hỗ trợ nhận diện giọng nói. Hãy mở web bằng <b>Google Chrome</b> hoặc <b>Microsoft Edge</b> (cần Internet và cho phép micro).</div>
  <div class="monTab" id="noiTab"></div>
  <div class="the" style="text-align:center">
    <span class="chip" id="noiSo"></span>
    <div class="cauNoi" id="cauNoi"></div>
    <div class="dk"><button class="nut phu2" onclick="noi(cauNoiHT)">🔊 Nghe mẫu</button>
    <button class="nut phu2" onclick="noi(cauNoiHT,0.6)">🐢 Nghe chậm</button></div>
    <button class="mic" id="mic" onclick="batMic()" style="margin-top:14px">🎙️</button>
    <p id="noiTrangThai" style="color:var(--mo)">Bấm micro và đọc to câu trên</p>
    <div id="noiKq"></div>
    <div class="dk" style="margin-top:10px"><button class="nut phu2" onclick="cauNoi(-1)">⬅ Câu trước</button>
    <button class="nut" onclick="cauNoi(1)">Câu tiếp ➜</button></div>
  </div>
  <div class="the" style="margin-top:18px"><h3 style="margin-top:0">💡 Mẹo luyện nói</h3>
  <ul style="line-height:1.8;margin:0"><li>Nghe mẫu 2–3 lần, chú ý trọng âm và ngữ điệu.</li>
  <li>Đọc to, rõ ràng, tốc độ vừa phải, đứng gần micro.</li>
  <li>Từ bị tô đỏ là từ máy chưa nghe rõ — hãy luyện riêng từ đó.</li>
  <li>Phát âm rõ âm cuối: /s/, /t/, /d/, /ed/.</li></ul></div>
</section>
</div>

<!-- ===================== MODAL ĐĂNG NHẬP / ĐĂNG KÝ ===================== -->
<div id="modalAuth" class="modal-overlay an">
  <div class="modal-box">
    <h2 id="authTieuDe">Đăng nhập tài khoản</h2>
    <p class="phu" id="authPhu">Nhập thông tin để đồng bộ kết quả ôn thi của bạn.</p>
    <form id="formAuth" onsubmit="xuLyAuth(event)">
      <div class="form-nhom" id="nhomTen" style="display:none">
        <label>Họ và tên</label>
        <input type="text" id="authHoTen" placeholder="Ví dụ: Nguyễn Văn A">
      </div>
      <div class="form-nhom">
        <label>Tên đăng nhập hoặc Email</label>
        <input type="text" id="authEmail" placeholder="Nhập tên đăng nhập..." required>
      </div>
      <div class="form-nhom">
        <label>Mật khẩu</label>
        <input type="password" id="authMatKhau" placeholder="Nhập mật khẩu..." required>
      </div>
      <div class="form-loi" id="authLoi"></div>
      <button type="submit" class="nut" style="width:100%" id="authNutSubmit">Đăng nhập</button>
    </form>
    <div class="form-chuyen" id="authChuyenTrang">
      Chưa có tài khoản? <a onclick="doiCheDoAuth('dangky')">Đăng ký ngay</a>
    </div>
  </div>
</div>

<button id="chatNut" onclick="moChat()">🤖<span>Hỏi trợ lý AI</span></button>
<div id="chatHop" class="an">
  <div class="chatDau"><div class="av">🤖</div><div><b>Thầy Cô AI</b><small id="chatCheDo">Trợ lý học tập</small></div>
  <button onclick="xoaChat()" title="Cuộc trò chuyện mới" style="margin-left:auto">🗑</button><button onclick="dongChat()" style="margin-left:6px">✕</button></div>
  <div id="chatThan"></div>
  <div id="chatGoiY"></div>
  <form id="chatForm"><textarea id="chatNhap" rows="1" placeholder="Hỏi bài Toán, Văn, Anh... (Enter để gửi)"></textarea><button type="submit">➤</button></form>
</div>
<footer>🎓 ÔnThi10 · Web ôn thi vào lớp 10 chạy bằng Python · Chúc bạn thi tốt!</footer>

<script>
const NGAY_THI = "__NGAY_THI__";
const $ = id => document.getElementById(id);
const api = async (u,o) => (await fetch(u,o)).json();
const MAU = {toan:'#e0e7ff', van:'#fce7f3', anh:'#d1fae5'};
function luu(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
function doc(k,md){try{return JSON.parse(localStorage.getItem(k))??md}catch(e){return md}}

/* ---------- hệ thống quản lý người dùng (Đăng nhập / Đăng ký) ---------- */
let nguoiDungHT = doc('nguoiDungHT', null);
let cheDoAuth = 'dangnhap';

function khoiTaoAuth(){
  const vung = $('vungAuth');
  if(nguoiDungHT){
    vung.innerHTML = `
      <div class="user-pill">👤 ${nguoiDungHT.ten || nguoiDungHT.email}</div>
      <button class="nut phu2 nho" onclick="dangXuat()">Đăng xuất</button>
    `;
  } else {
    vung.innerHTML = `
      <button class="nut phu2 nho" onclick="moModalAuth('dangnhap')">Đăng nhập</button>
      <button class="nut nho" onclick="moModalAuth('dangky')">Đăng ký</button>
    `;
  }
}

function moModalAuth(cheDo){
  cheDoAuth = cheDo;
  $('authLoi').textContent = '';
  $('formAuth').reset();
  if(cheDo === 'dangnhap'){
    $('authTieuDe').textContent = 'Đăng nhập tài khoản';
    $('authPhu').textContent = 'Nhập thông tin để đồng bộ kết quả ôn thi của bạn.';
    $('nhomTen').style.display = 'none';
    $('authNutSubmit').textContent = 'Đăng nhập';
    $('authChuyenTrang').innerHTML = 'Chưa có tài khoản? <a onclick="doiCheDoAuth(\'dangky\')">Đăng ký ngay</a>';
  } else {
    $('authTieuDe').textContent = 'Đăng ký tài khoản mới';
    $('authPhu').textContent = 'Tạo tài khoản để bắt đầu hành trình ôn thi vào lớp 10.';
    $('nhomTen').style.display = 'block';
    $('authNutSubmit').textContent = 'Đăng ký tài khoản';
    $('authChuyenTrang').innerHTML = 'Đã có tài khoản? <a onclick="doiCheDoAuth(\'dangnhap\')">Đăng nhập ngay</a>';
  }
  $('modalAuth').classList.remove('an');
}

function doiCheDoAuth(cheDo){ moModalAuth(cheDo); }
function dongModalAuth(){ $('modalAuth').classList.add('an'); }

function xuLyAuth(e){
  e.preventDefault();
  const email = $('authEmail').value.trim();
  const matKhau = $('authMatKhau').value.trim();
  const ten = $('authHoTen').value.trim();
  let dsUsers = doc('danhSachUsers10', []);

  if(cheDoAuth === 'dangky'){
    if(!ten){ $('authLoi').textContent = 'Vui lòng nhập họ tên!'; return; }
    if(dsUsers.find(u => u.email === email)){
      $('authLoi').textContent = 'Tên đăng nhập hoặc Email này đã tồn tại!';
      return;
    }
    const userMoi = { email, matKhau, ten };
    dsUsers.push(userMoi);
    luu('danhSachUsers10', dsUsers);
    nguoiDungHT = userMoi;
    luu('nguoiDungHT', nguoiDungHT);
    dongModalAuth();
    khoiTaoAuth();
    capNhatTK();
  } else {
    const user = dsUsers.find(u => u.email === email && u.matKhau === matKhau);
    if(!user){
      $('authLoi').textContent = 'Tên đăng nhập hoặc mật khẩu không chính xác!';
      return;
    }
    nguoiDungHT = user;
    luu('nguoiDungHT', nguoiDungHT);
    dongModalAuth();
    khoiTaoAuth();
    capNhatTK();
  }
}

function dangXuat(){
  nguoiDungHT = null;
  localStorage.removeItem('nguoiDungHT');
  khoiTaoAuth();
  capNhatTK();
}

/* ---------- điều hướng ---------- */
document.querySelectorAll('.tab[data-t]').forEach(b=>b.onclick=()=>moTab(b.dataset.t));
function moTab(t,mon){
  document.querySelectorAll('.tab[data-t]').forEach(b=>b.classList.toggle('on',b.dataset.t===t));
  document.querySelectorAll('.trang').forEach(s=>s.classList.toggle('on',s.id===t));
  if(t==='lythuyet'&&mon) chonMonLT(mon);
  if(t==='home') capNhatTK();
  speechSynthesis.cancel(); scrollTo({top:0,behavior:'smooth'});
}

/* ---------- đếm ngược ---------- */
function demNguoc(){
  let s=Math.max(0,(new Date(NGAY_THI+'T07:00:00')-new Date())/1000);
  const d=Math.floor(s/86400),h=Math.floor(s%86400/3600),m=Math.floor(s%3600/60),g=Math.floor(s%60);
  $('demNguoc').innerHTML=`<div><b>${d}</b><span>ngày</span></div><div><b>${h}</b><span>giờ</span></div><div><b>${m}</b><span>phút</span></div><div><b>${g}</b><span>giây</span></div><div style="text-align:left;background:none"><span>đến kỳ thi<br>${NGAY_THI.split('-').reverse().join('/')}</span></div>`;
}
setInterval(demNguoc,1000); demNguoc();

/* ---------- thống kê & lịch sử ---------- */
function capNhatTK(){
  const ls=doc('ls10',[]);
  $('tkBai').textContent=ls.length;
  $('tkTB').textContent=ls.length?(ls.reduce((a,x)=>a+x.diem,0)/ls.length).toFixed(1):0;
  $('tkCao').textContent=ls.length?Math.max(...ls.map(x=>x.diem)):0;
  $('tkNoi').textContent=doc('soNoi',0);
  if(ls.length) $('lichSu').innerHTML='<table class="bang"><tr><th>Môn</th><th>Điểm</th><th>Thời gian</th></tr>'+
    ls.slice(0,10).map(x=>`<tr><td>${x.mon}</td><td><b style="color:${x.diem>=8?'#10b981':x.diem>=5?'#f59e0b':'#ef4444'}">${x.diem}</b></td><td>${x.luc}</td></tr>`).join('')+'</table>';
}

/* ================= LÝ THUYẾT ================= */
let LT={}, monLT='toan', dsLT=[];
const TENMON={toan:'📐 Toán',van:'📖 Ngữ văn',anh:'🇬🇧 Tiếng Anh'};
async function taiLT(){
  LT=await api('/api/lythuyet');
  $('ltTab').innerHTML=Object.keys(LT).map(k=>`<button class="nut phu2" data-m="${k}" onclick="chonMonLT('${k}')">${TENMON[k]}</button>`).join('');
  chonMonLT('toan');
}
function chonMonLT(m){
  monLT=m; $('ltTim').value='';
  document.querySelectorAll('#ltTab .nut').forEach(b=>b.classList.toggle('phu2',b.dataset.m!==m));
  veLT();
}
function veLT(){
  const q=$('ltTim').value.toLowerCase();
  const ds=dsLT=(LT[monLT]||[]).filter(x=>!q||(x.ten+x.noi_dung).toLowerCase().includes(q));
  $('ltDs').innerHTML=ds.length?ds.map((x,i)=>`<div class="the acc ${i===0&&!q?'mo':''}">
    <button onclick="this.parentElement.classList.toggle('mo')"><span class="so">${i+1}</span>${x.ten}<span class="mt">▼</span></button>
    <div class="nd">${x.noi_dung}<button class="nut phu2 nho" onclick="hoiLT(${i})">🤖 Hỏi AI thêm về chuyên đề này</button></div></div>`).join(''):'<p class="phu">Không tìm thấy chuyên đề phù hợp.</p>';
}
$('ltTim').oninput=veLT;

/* ================= LUYỆN ĐỀ ================= */
let monHT=null, de=[], dongHo=null, conLai=0, kqCuoi=[];
async function taiMon(){
  const ds=await api('/api/mon');
  $('dsMon').innerHTML=ds.map(m=>`<div class="the mon" onclick="batDau('${m.ma}')">
    <div class="ic" style="background:${MAU[m.ma]}">${m.icon}</div><h3>${m.ten}</h3>
    <p>${m.so_cau} câu · ${m.thoi_gian} phút</p><br><span class="chip">Bắt đầu làm bài →</span></div>`).join('');
}
function veChonDe(){['deChon','deLam','deKq'].forEach(x=>$(x).classList.toggle('an',x!=='deChon'))}
async function batDau(ma){
  monHT=ma; const d=await api('/api/de/'+ma); de=d.cau;
  $('tenMon').textContent=d.icon+' '+d.ten;
  $('dsCau').innerHTML=de.map((c,i)=>`<div class="the q"><h4>Câu ${i+1}. ${c.hoi}</h4>`+
    c.lua_chon.map((l,j)=>`<label class="opt"><input type="radio" name="c${i}" value="${j}"><span class="kt">${'ABCD'[j]}</span>${l}</label>`).join('')+'</div>').join('');
  document.querySelectorAll('#dsCau input').forEach(r=>r.onchange=()=>{
    document.querySelectorAll(`input[name=${r.name}]`).forEach(x=>x.parentElement.classList.toggle('chon',x.checked));
    tienDo();});
  tienDo();
  conLai=d.thoi_gian*60; clearInterval(dongHo); gio();
  dongHo=setInterval(()=>{conLai--;gio();if(conLai<=0){nopBai();alert('⏰ Hết giờ! Bài đã được nộp tự động.')}},1000);
  ['deChon','deLam','deKq'].forEach(x=>$(x).classList.toggle('an',x!=='deLam')); scrollTo(0,0);
}
function tienDo(){const n=document.querySelectorAll('#dsCau input:checked').length;
  $('tienDo').style.width=(n/de.length*100)+'%'; $('daLam').textContent=`${n}/${de.length} câu`}
function gio(){const m=Math.floor(conLai/60),s=conLai%60;$('gio').textContent=`⏰ ${m}:${String(s).padStart(2,'0')}`}
async function nopBai(){
  clearInterval(dongHo);
  const tl=de.map((c,i)=>{const r=document.querySelector(`input[name=c${i}]:checked`);return{id:c.id,chon:r?+r.value:-1}});
  const kq=await api('/api/cham',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mon:monHT,tra_loi:tl})});
  $('kqMon').textContent='Kết quả môn '+kq.ten;
  $('kqDiem').textContent=kq.diem;
  const mau=kq.diem>=8?'#10b981':kq.diem>=5?'#f59e0b':'#ef4444';
  $('kqVong').style.background=`conic-gradient(${mau} ${kq.diem*36}deg,#e2e8f0 0)`;
  $('kqDiem').style.color=mau;
  $('kqNx').textContent=`Đúng ${kq.dung}/${kq.tong} câu — `+(kq.diem>=9?'Xuất sắc! 🏆':kq.diem>=7?'Khá tốt! 👍':kq.diem>=5?'Đạt, cần ôn thêm 📚':'Cố gắng hơn nhé 💪');
  kqCuoi=kq.chi_tiet;
  $('kqCt').innerHTML=kq.chi_tiet.map((c,i)=>`<div class="the q"><h4>Câu ${i+1}. ${c.hoi} ${c.chon===c.dap_an?'✅':'❌'}</h4>`+
    c.lua_chon.map((l,j)=>`<div class="opt ${j===c.dap_an?'dung':(j===c.chon?'sai':'')}"><span class="kt">${'ABCD'[j]}</span>${l}</div>`).join('')+
    `<div class="giai">${c.chon===-1?'⚠️ Bạn chưa chọn đáp án. ':''}💡 ${c.giai}</div>
    <button class="nut phu2 nho" onclick="hoiCau(${i})">🤖 Nhờ AI giải thích kỹ hơn</button></div>`).join('');
  const ls=doc('ls10',[]); ls.unshift({mon:kq.ten,diem:kq.diem,luc:new Date().toLocaleString('vi-VN')}); luu('ls10',ls.slice(0,50));
  ['deChon','deLam','deKq'].forEach(x=>$(x).classList.toggle('an',x!=='deKq')); scrollTo(0,0);
  if(kq.diem>=8) phaoHoa();
}

/* ================= GIỌNG ĐỌC (Text-to-Speech) ================= */
let dsGiong=[];
function taiGiong(){
  dsGiong=speechSynthesis.getVoices().filter(v=>v.lang.startsWith('en'));
  $('giong').innerHTML=dsGiong.map((v,i)=>`<option value="${i}">${v.name} (${v.lang})</option>`).join('')||'<option>Mặc định</option>';
  const us=dsGiong.findIndex(v=>v.lang==='en-US'); if(us>=0)$('giong').value=us;
}
speechSynthesis.onvoiceschanged=taiGiong; taiGiong();
function noi(text,toc,songId,loaId){
  speechSynthesis.cancel();
  const u=new SpeechSynthesisUtterance(text);
  u.lang='en-US'; u.rate=toc||+$('tocDo').value;
  const v=dsGiong[+$('giong').value]; if(v)u.voice=v;
  if(songId){$(songId).classList.add('chay');$(loaId).classList.add('dang');
    u.onend=u.onerror=()=>{$(songId).classList.remove('chay');$(loaId).classList.remove('dang')}}
  speechSynthesis.speak(u);
}
function dungDoc(){speechSynthesis.cancel();['song1','song2'].forEach(x=>$(x).classList.remove('chay'));['loa1','loa2'].forEach(x=>$(x).classList.remove('dang'))}

/* ================= LUYỆN NGHE ================= */
let BN=[], CHEP=[], baiHT=0, chepHT=0;
async function taiNghe(){
  const d=await api('/api/nghe'); BN=d.bai; CHEP=d.chep;
  $('dsBaiNghe').innerHTML=BN.map((b,i)=>`<button class="nut phu2" data-i="${i}" onclick="chonBai(${i})">Bài ${i+1}: ${b.tieu_de}</button>`).join('');
  chonBai(0); cauChep(0);
}
function cheDoNghe(n){$('nghe1').classList.toggle('an',n!==1);$('nghe2').classList.toggle('an',n!==2);
  $('ngheTab1').classList.toggle('phu2',n!==1);$('ngheTab2').classList.toggle('phu2',n!==2);dungDoc()}
function chonBai(i){
  baiHT=i; dungDoc(); const b=BN[i];
  document.querySelectorAll('#dsBaiNghe .nut').forEach(x=>x.classList.toggle('phu2',+x.dataset.i!==i));
  $('ngheTen').textContent=b.tieu_de; $('ngheMuc').textContent='Mức độ: '+b.muc_do;
  $('loiBai').textContent=b.doan; $('loiBai').classList.add('an'); $('ngheKq').textContent='';
  $('ngheCau').innerHTML=b.cau.map((c,k)=>`<div class="the q"><h4>${k+1}. ${c.hoi}</h4>`+
    c.lua_chon.map((l,j)=>`<label class="opt"><input type="radio" name="n${k}" value="${j}"><span class="kt">${'ABCD'[j]}</span>${l}</label>`).join('')+'</div>').join('');
  document.querySelectorAll('#ngheCau input').forEach(r=>r.onchange=()=>
    document.querySelectorAll(`input[name=${r.name}]`).forEach(x=>x.parentElement.classList.toggle('chon',x.checked)));
}
function docBai(){noi(BN[baiHT].doan,null,'song1','loa1')}
function hienLoi(){$('loiBai').classList.toggle('an')}
function chamNghe(){
  const b=BN[baiHT]; let d=0;
  b.cau.forEach((c,k)=>{
    const r=document.querySelector(`input[name=n${k}]:checked`), chon=r?+r.value:-1;
    if(chon===c.dap_an)d++;
    document.querySelectorAll(`input[name=n${k}]`).forEach((x,j)=>{const o=x.parentElement;o.classList.remove('chon');
      o.classList.toggle('dung',j===c.dap_an);o.classList.toggle('sai',j===chon&&chon!==c.dap_an)});
  });
  $('ngheKq').innerHTML=`🎯 Bạn đúng ${d}/${b.cau.length} câu ${d===b.cau.length?'— Tuyệt vời! 🎉':''}`;
  if(d===b.cau.length)phaoHoa();
}
function cauChep(buoc){
  chepHT=(chepHT+buoc+CHEP.length)%CHEP.length;
  $('chepSo').textContent=`Câu ${chepHT+1}/${CHEP.length}`; $('chepNhap').value=''; $('chepKq').innerHTML='';
}
function docChep(){noi(CHEP[chepHT],null,'song2','loa2')}
const chuan=s=>s.toLowerCase().replace(/[^a-z0-9' ]/g,' ').split(/\s+/).filter(Boolean);
function kiemTraChep(){
  const goc=CHEP[chepHT], a=chuan(goc), b=chuan($('chepNhap').value);
  const {khop,diem}=soSanh(a,b);
  $('chepKq').innerHTML=`<p><b>Đáp án:</b> ${a.map((w,i)=>`<span class="tu ${khop[i]?'d':'s'}">${w}</span>`).join('')}</p>
  <p style="font-size:20px;font-weight:700;color:${diem>=80?'#10b981':'#f59e0b'}">${diem}% chính xác ${diem===100?'🎉':''}</p>`;
  if(diem===100)phaoHoa();
}
$('chepNhap').addEventListener('keydown',e=>{if(e.key==='Enter')kiemTraChep()});

/* So khớp từ theo dãy con chung dài nhất (LCS) */
function soSanh(a,b){
  const n=a.length,m=b.length,L=Array.from({length:n+1},()=>Array(m+1).fill(0));
  for(let i=n-1;i>=0;i--)for(let j=m-1;j>=0;j--)L[i][j]=a[i]===b[j]?L[i+1][j+1]+1:Math.max(L[i+1][j],L[i][j+1]);
  const khop=Array(n).fill(false);let i=0,j=0;
  while(i<n&&j<m){if(a[i]===b[j]){khop[i]=true;i++;j++}else if(L[i+1][j]>=L[i][j+1])i++;else j++}
  const dung=khop.filter(Boolean).length, thua=Math.max(0,m-dung);
  return {khop,diem:Math.max(0,Math.round((dung-thua*0.25)/n*100))};
}

/* ================= LUYỆN NÓI ================= */
let BNOI={}, nhomNoi='', iNoi=0, cauNoiHT='', nhanDien=null, dangGhi=false;
const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
async function taiNoi(){
  BNOI=await api('/api/noi');
  $('noiTab').innerHTML=Object.keys(BNOI).map(k=>`<button class="nut phu2" data-k="${k}" onclick="chonNhom('${k}')">${k}</button>`).join('');
  chonNhom(Object.keys(BNOI)[0]);
  if(!SR){$('noiBao').classList.remove('an');$('mic').disabled=true;$('mic').style.opacity=.4}
}
function chonNhom(k){nhomNoi=k;iNoi=0;document.querySelectorAll('#noiTab .nut').forEach(b=>b.classList.toggle('phu2',b.dataset.k!==k));cauNoi(0)}
function cauNoi(buoc){
  const ds=BNOI[nhomNoi]; iNoi=(iNoi+buoc+ds.length)%ds.length; cauNoiHT=ds[iNoi];
  $('cauNoi').textContent=cauNoiHT; $('noiSo').textContent=`${nhomNoi} · ${iNoi+1}/${ds.length}`;
  $('noiKq').innerHTML=''; $('noiTrangThai').textContent='Bấm micro và đọc to câu trên';
}
function batMic(){
  if(!SR)return;
  if(dangGhi){nhanDien.stop();return}
  speechSynthesis.cancel();
  nhanDien=new SR(); nhanDien.lang='en-US'; nhanDien.interimResults=true; nhanDien.maxAlternatives=3;
  let ketQua='';
  nhanDien.onstart=()=>{dangGhi=true;$('mic').classList.add('ghi');$('mic').textContent='⏹';$('noiTrangThai').textContent='🔴 Đang nghe... hãy đọc to'};
  nhanDien.onresult=e=>{ketQua=[...e.results].map(r=>r[0].transcript).join(' ');$('noiTrangThai').textContent='🗣️ '+ketQua};
  nhanDien.onerror=e=>{$('noiTrangThai').textContent=e.error==='not-allowed'?'❌ Bạn chưa cho phép dùng micro.':e.error==='no-speech'?'🤔 Không nghe thấy gì, thử lại nhé.':'❌ Lỗi: '+e.error+' (cần Internet)'};
  nhanDien.onend=()=>{dangGhi=false;$('mic').classList.remove('ghi');$('mic').textContent='🎙️';if(ketQua)chamNoi(ketQua)};
  nhanDien.start();
}
function chamNoi(noiDuoc){
  const a=chuan(cauNoiHT), {khop,diem}=soSanh(a,chuan(noiDuoc));
  const mau=diem>=85?'#10b981':diem>=60?'#f59e0b':'#ef4444';
  $('noiKq').innerHTML=`<div class="vong" style="width:130px;height:130px;background:conic-gradient(${mau} ${diem*3.6}deg,#e2e8f0 0)">
    <div style="width:104px;height:104px;font-size:30px;color:${mau}">${diem}</div></div>
    <p>${a.map((w,i)=>`<span class="tu ${khop[i]?'d':'s'}">${w}</span>`).join('')}</p>
    <p style="font-weight:700;font-size:18px">${diem>=85?'Phát âm rất tốt! 🌟':diem>=60?'Khá ổn, luyện thêm các từ màu đỏ nhé 👍':'Hãy nghe mẫu và thử lại 💪'}</p>
    <p style="color:var(--mo)">Máy nghe được: "<i>${noiDuoc}</i>"</p>`;
  $('noiTrangThai').textContent='';
  luu('soNoi',doc('soNoi',0)+1);
  if(diem>=85)phaoHoa();
}

/* ================= PHÁO HOA ================= */
function phaoHoa(){
  const c=$('phao'),x=c.getContext('2d');c.width=innerWidth;c.height=innerHeight;
  const mau=['#6366f1','#ec4899','#10b981','#f59e0b','#8b5cf6','#06b6d4'];
  const ht=Array.from({length:160},()=>({x:innerWidth/2,y:innerHeight/3,vx:(Math.random()-.5)*16,vy:Math.random()*-14-3,
    r:Math.random()*6+3,m:mau[Math.floor(Math.random()*mau.length)],g:Math.random()*360}));
  let t=0;(function ve(){x.clearRect(0,0,c.width,c.height);
    ht.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.vy+=.4;p.vx*=.99;p.g+=8;x.save();x.translate(p.x,p.y);x.rotate(p.g*Math.PI/180);
      x.fillStyle=p.m;x.fillRect(-p.r/2,-p.r/2,p.r,p.r*1.6);x.restore()});
    if(++t<130)requestAnimationFrame(ve);else x.clearRect(0,0,c.width,c.height)})();
}

/* ================= TRỢ LÝ AI ================= */
let lichSuChat=doc('chat10',[]), dangGui=false;
const GOI_Y=['Giải phương trình x² − 5x + 6 = 0','Hệ thức Vi-ét dùng để làm gì?','Dàn ý đoạn văn nghị luận 200 chữ',
  'Phân biệt hiện tại hoàn thành và quá khứ đơn','Lập kế hoạch ôn thi trong 1 tháng','Cách làm câu hỏi biện pháp tu từ'];
function md(t){
  let h=t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  h=h.replace(/```\w*\n?([\s\S]*?)```/g,(m,c)=>'<pre>'+c.replace(/\n/g,'\u0001')+'</pre>');
  h=h.replace(/`([^`\n]+)`/g,'<code>$1</code>').replace(/\*\*(.+?)\*\*/g,'<b>$1</b>')
     .replace(/(^|[^*\w])[*_]([^*_\n]+)[*_](?=[^*\w]|$)/g,'$1<i>$2</i>')
     .replace(/^#{1,6} (.+)$/gm,'<span class="h">$1</span>')
     .replace(/^\s*[-*•] (.+)$/gm,'<li>$1</li>').replace(/^\s*(\d+)\. (.+)$/gm,'<li style="list-style:none"><b>$1.</b> $2</li>');
  return h.replace(/\n/g,'<br>').replace(/<\/li><br>/g,'</li>').replace(/<\/span><br>/g,'</span>').replace(/\u0001/g,'\n');
}
function themTin(vai,noiDung,laHtml){
  const d=document.createElement('div'); d.className='tin '+(vai==='user'?'user':'bot');
  if(laHtml)d.innerHTML=noiDung; else if(vai==='user')d.textContent=noiDung; else d.innerHTML=md(noiDung);
  $('chatThan').appendChild(d); $('chatThan').scrollTop=$('chatThan').scrollHeight; return d;
}
function veChat(){
  $('chatThan').innerHTML='';
  themTin('bot','Chào bạn! 👋 Mình là **Thầy Cô AI**, trợ lý ôn thi vào lớp 10.\nBạn có thể hỏi mình:\n- 📐 Giải bài **Toán** từng bước\n- 📖 Lập dàn ý, góp ý bài **Ngữ văn**\n- 🇬🇧 Giải thích ngữ pháp, sửa câu **Tiếng Anh**\nHãy chọn gợi ý bên dưới hoặc gõ câu hỏi nhé!');
  lichSuChat.forEach(m=>themTin(m.role,m.content));
  $('chatGoiY').innerHTML=GOI_Y.map(g=>`<button type="button">${g}</button>`).join('');
  document.querySelectorAll('#chatGoiY button').forEach(b=>b.onclick=()=>guiChat(b.textContent));
}
async function capNhatCheDo(){
  try{const r=await api('/api/chat/trangthai');
    $('chatCheDo').textContent=r.che_do==='ai'?'🟢 Đang dùng AI':'🟡 Chế độ offline (chưa bật AI)';
    $('chatCheDo').title=r.ly_do;}catch(e){}
}
function moChat(){ $('chatHop').classList.remove('an'); $('chatNut').classList.add('an'); setTimeout(()=>$('chatNhap').focus(),100) }
function dongChat(){ $('chatHop').classList.add('an'); $('chatNut').classList.remove('an') }
function xoaChat(){ lichSuChat=[]; luu('chat10',[]); veChat() }
async function guiChat(text){
  text=(text||'').trim(); if(!text||dangGui)return;
  moChat(); themTin('user',text); lichSuChat.push({role:'user',content:text});
  dangGui=true; const cho=themTin('bot','<span class="go"><i></i><i></i><i></i></span>',true);
  try{
    const r=await api('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({messages:lichSuChat.slice(-20)})});
    cho.innerHTML=md(r.reply); lichSuChat.push({role:'assistant',content:r.reply});
    luu('chat10',lichSuChat.slice(-40));
  }catch(e){ cho.innerHTML='❌ Không kết nối được máy chủ. Hãy kiểm tra cửa sổ Python còn đang chạy không.'; lichSuChat.pop() }
  dangGui=false; $('chatThan').scrollTop=$('chatThan').scrollHeight;
}
$('chatForm').onsubmit=e=>{e.preventDefault();const t=$('chatNhap').value;$('chatNhap').value='';$('chatNhap').style.height='';guiChat(t)};
$('chatNhap').addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();$('chatForm').requestSubmit()}});
$('chatNhap').addEventListener('input',function(){this.style.height='';this.style.height=Math.min(this.scrollHeight,110)+'px'});
function hoiLT(i){const x=dsLT[i];guiChat(`Giảng giải thêm cho mình về chuyên đề "${x.ten}" (môn ${TENMON[monLT].slice(3)}), kèm ví dụ minh họa và 1 bài tập tự luyện.`)}
function hoiCau(i){
  const c=kqCuoi[i], L='ABCD';
  guiChat(`Giải thích giúp mình câu này:\n"${c.hoi}"\n`+c.lua_chon.map((l,j)=>`${L[j]}. ${l}`).join('\n')+
    `\nMình ${c.chon===-1?'chưa chọn':'đã chọn '+L[c.chon]}, đáp án đúng là ${L[c.dap_an]}. Vì sao vậy?`);
}

khoiTaoAuth();
veChat(); capNhatCheDo();

taiLT(); taiMon(); taiNghe(); taiNoi(); capNhatTK();
</script></body></html>"""


# ==============================================================
# 7. MÁY CHỦ WEB
# ==============================================================
class XuLy(BaseHTTPRequestHandler):
    def gui(self, noi_dung, loai="application/json", ma=200):
        data = noi_dung.encode("utf-8")
        self.send_response(ma)
        self.send_header("Content-Type", loai + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def gui_json(self, obj, ma=200):
        self.gui(json.dumps(obj, ensure_ascii=False), ma=ma)

    def do_GET(self):
        p = self.path.split("?")[0]
        if p in ("/", "/index.html"):
            self.gui(HTML.replace("__NGAY_THI__", NGAY_THI), "text/html")
        elif p == "/api/lythuyet":
            self.gui_json(LY_THUYET)
        elif p == "/api/nghe":
            self.gui_json({"bai": BAI_NGHE, "chep": NGHE_CHEP})
        elif p == "/api/noi":
            self.gui_json(BAI_NOI)
        elif p == "/api/chat/trangthai":
            duoc, ly_do = co_ai()
            self.gui_json({"che_do": "ai" if duoc else "offline", "ly_do": ly_do})
        elif p == "/api/mon":
            self.gui_json([{"ma": k, "ten": v["ten"], "icon": v["icon"],
                            "so_cau": min(10, len(v["cau"])), "thoi_gian": v["thoi_gian"]}
                           for k, v in CAU_HOI.items()])
        elif p.startswith("/api/de/"):
            ma = p.split("/")[-1]
            if ma not in CAU_HOI:
                return self.gui_json({"loi": "Không có môn này"}, 404)
            mon = CAU_HOI[ma]
            chon = random.sample(range(len(mon["cau"])), min(10, len(mon["cau"])))  # bốc ngẫu nhiên 10 câu
            cau = [{"id": i, "hoi": mon["cau"][i]["hoi"], "lua_chon": mon["cau"][i]["lua_chon"]} for i in chon]
            self.gui_json({"ten": mon["ten"], "icon": mon["icon"], "thoi_gian": mon["thoi_gian"], "cau": cau})
        else:
            self.gui_json({"loi": "Không tìm thấy"}, 404)

    def do_POST(self):
        do_dai = int(self.headers.get("Content-Length", 0))
        try:
            du_lieu = json.loads(self.rfile.read(do_dai).decode("utf-8"))
        except ValueError:
            return self.gui_json({"loi": "Dữ liệu không hợp lệ"}, 400)
        if self.path == "/api/chat":
            return self.gui_json(xu_ly_chat(du_lieu))
        if self.path != "/api/cham":
            return self.gui_json({"loi": "Không tìm thấy"}, 404)
        mon = CAU_HOI.get(du_lieu.get("mon"))
        if not mon:
            return self.gui_json({"loi": "Không có môn này"}, 400)
        dung, chi_tiet = 0, []
        for tl in du_lieu.get("tra_loi", []):
            c = mon["cau"][int(tl["id"])]
            if tl["chon"] == c["dap_an"]:
                dung += 1
            chi_tiet.append({**c, "chon": tl["chon"]})
        tong = len(chi_tiet) or 1
        self.gui_json({"ten": mon["ten"], "dung": dung, "tong": tong,
                       "diem": round(dung / tong * 10, 1), "chi_tiet": chi_tiet})

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    try:
        import sys
        sys.stdout.reconfigure(encoding="utf-8")  # tránh lỗi in tiếng Việt/emoji trên Windows
    except Exception:
        pass
    # Nếu cổng 8000 đang bị chương trình cũ chiếm thì tự chuyển sang cổng kế tiếp
    may_chu = None
    for cong in range(PORT, PORT + 20):
        try:
            may_chu = ThreadingHTTPServer(("0.0.0.0", cong), XuLy)
            break
        except OSError:
            print(f"  ⚠️ Cổng {cong} đang bị chương trình khác dùng, thử cổng {cong + 1}...")
    if may_chu is None:
        raise SystemExit("Không tìm được cổng trống. Hãy tắt các chương trình Python đang chạy rồi thử lại.")
    url = f"http://localhost:{cong}"
    print("=" * 56)
    print("  🎓 WEB ÔN THI VÀO LỚP 10 ĐANG CHẠY")
    print(f"  👉 Mở trình duyệt tại: {url}")
    print("  🎤 Luyện nói: dùng Chrome/Edge và cho phép micro")
    _duoc, _ly_do = co_ai()
    print("  🤖 Trợ lý AI: " + ("BẬT - " + MODEL_AI if _duoc else "OFFLINE - " + _ly_do))
    print("  ⛔ Nhấn Ctrl + C để dừng")
    print("=" * 56)
    threading.Timer(1, lambda: webbrowser.open(url)).start()
    try:
        may_chu.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng web")