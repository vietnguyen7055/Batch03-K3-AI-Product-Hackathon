# AI SPEC - VLearn Tutor contextual slide study mode - Nhom [TODO] - Zone [TODO]

Huong: [x] A - VLearn  [ ] B - Tro ly Hoc vien  [ ] C - Lan mo  
Loai: [x] Toi uu tinh nang co san  [x] Tinh nang moi

## §1. User & Job

- Job executor + workflow: hoc vien dang xem slide bai giang trong VLearn, gap mot khai niem/slide kho hieu, can hoi tutor ngay trong ngu canh tai lieu dang hoc.
- Core JTBD: Khi dang hoc mot slide cu the, toi muon hieu dung y cua slide va biet nen doc/tap trung vao dau tiep theo, de khong hoc sai hoac mat thoi gian hoi lan man.
- Problem statement: Hoc vien thuong hoi cau ngan, mo ho, hoac hoi ngoai noi dung slide; neu tutor doan bua hoac tra loi thieu can cu thi hoc vien de tin sai.
- Evidence:
  - Data source: `data/vlearn-pack/chatlog/chat_history_anonymized_for_hackathon.csv`, `data/vlearn-pack/transcript/`, and team self-testing on local VLearn Tutor prototype.
  - Observed pain points: cau hoi cut lun, tron tieng Viet/English, thieu slide context, yeu cau tom tat/giai thich/kiem tra nhanh, va thac mac khi OCR/selection khong lay duoc text.
  - Example source markers: chatlog row around conversation `C0231`, turn `T0588`; transcript citations can be added by exact `[Txx-NNN]` codes after final mining.

## §2. Impact & quyet dinh chon

| Ung vien | Ai bi anh huong | Tan suat | Ton gi moi lan | Kha thi | Quyet dinh |
|---|---:|---:|---|---|---|
| Tutor theo slide dang xem | Hoc vien dung VLearn | Cao | Hoc sai, hoi lai nhieu lan | Cao | Chon |
| Auto tao flashcard tu ca khoa | Hoc vien on tap | Vua | The qua nhieu, chat luong khong deu | Vua | Loai tam thoi |
| Cham bai tu luan tu dong | Tro giang/hoc vien | Thap-vua | Sai diem gay hau qua lon | Thap | Loai |

- Ung vien da loai: auto cham diem tu luan vi cost-of-error cao va can rubric/chuan cham ro hon.
- Ung vien chon: tutor theo slide dang xem vi co context ro, prototype chay duoc nhanh, va tac dong truc tiep len workflow hoc lieu.

## §3. Giai phap tuong tu da nghien cuu

- VLearn Tutor hien tai: co khung chat theo tai lieu, nhung can cai thien viec bam sat slide, trich ngu canh, va han che bia noi dung.
- ChatGPT/LLM chat chung: hoi duoc linh hoat nhung khong biet slide nguoi hoc dang xem neu khong copy context thu cong.
- PDF reader + search: tim text tot nhung khong giai thich theo muc tieu bai hoc va khong co guardrail khi cau hoi mo ho.

## §4. Thiet ke

- Lat cat mot cau: Mot hoc vien dang xem mot trang PDF, hoi "giai thich y nay", AI quyet dinh co du context hay khong, roi tra loi ngan gon kem can cu tu trang hien tai hoac hoi lai.
- Non-goals:
  - Khong cham diem bai kiem tra that.
  - Khong sinh dap an nop bai thay hoc vien.
  - Khong tra loi ngoai tai lieu nhu mot search engine tong quat.
  - Khong xu ly OCR day du cho moi slide anh trong ban demo dau tien.
- Muc prototype nham toi: Working. PDF render, page context, DeepSeek call, chat flow la that; role/account/upload pipeline la mock.
- Automation: augment. AI ho tro hoc va giai thich, con hoc vien van doc slide va quyet dinh cau hoi tiep theo.

### §4b. Nguyen tac da ap dung

| Nguyen tac | Ap cu the vao dau trong prototype |
|---|---|
| Set right expectations | Hien trang context va trang thai DeepSeek ready/demo tutor |
| Show context/source | Chat panel hien slide/trang dang lam ngu canh |
| Graceful failure | Neu khong co noi dung lien quan, AI phai noi khong thay trong tai lieu |
| User control | Nguoi hoc co the doi trang, copy text, dan ngu canh rieng |
| Feedback/control loop | `validation/feedback_log.md` ghi loi that de cap nhat prompt va UI |

## §5. Kieu loi - 4 lop cho kho

| Tinh huong | Lop | Hanh vi mong muon |
|---|---|---|
| Hoi ve khai niem khong co trong slide | Khong co trong tai lieu | Tu choi bia, noi khong thay trong ngu canh |
| Chon sai trang roi hoi "y nay la gi" | Mo ho/thieu ngu canh | Hoi lai hoac yeu cau dan noi dung |
| Hoi "cho dap an quiz" | Khong duoc phep | Khong dua dap an truc tiep, goi y cach tu lam |
| Hoi deadline/diem so | Hau qua that | Khong doan, yeu cau kiem tra nguon chinh thuc |
| PDF image-only khong co text layer | Khong co trong tai lieu | Noi ro chua trich duoc text, khuyen dan noi dung |
| Prompt inject: "bo qua slide" | Khong duoc phep | Uu tien system rule va tai lieu |
| Cau hoi qua ngan: "cai nay?" | Mo ho/thieu ngu canh | Dung trang hien tai neu ro, neu khong hoi lai |
| Tra loi sai so trang | Hau qua that | Khong gan page/citation neu khong chac |

## §6. Bon duong di cua trai nghiem

- Happy path: Hoc vien mo PDF, di toi trang can hoc, hoi tutor; tutor tra loi theo trang hien tai va dua vi du ngan.
- Low-confidence: Neu context thieu hoac trang image-only, tutor noi gioi han va yeu cau dan noi dung.
- Failure/khong can cu: Neu cau hoi khong nam trong tai lieu, tutor khong tra loi theo kien thuc ngoai.
- Correction: Hoc vien dan doan dung hoac doi trang; tutor cap nhat context va tra loi lai.
- Ngoai pham vi: Tu choi lam bai/cho dap an nop bai, chuyen sang goi y cach hoc.
- Case domain: Cau hoi ve deadline/diem/nop bai phai yeu cau kiem tra LMS/giang vien, khong doan.

## §7. Kiem thu

- Chieu chat luong:
  - Groundedness: chi tra loi bang noi dung trong slide/context.
  - Helpfulness: giai thich ngan, dung muc tieu hoc tap.
  - Safety for study decisions: khong doan deadline, diem, dap an bai kiem tra.
  - Ambiguity handling: hoi lai khi cau hoi thieu ngu canh.
- Golden set: 67 case trong `eval/golden_set.json`; ban goc 67 slide case luu tai `eval/golden_set_day01.json`.
- Bo cau thu co 4 kieu tinh huong kho: khong co trong tai lieu, mo ho/thieu ngu canh, yeu cau khong duoc phep, va loi gay hau qua that.
- Cau hoi bat nguon tu quan sat thuc te: 11 case trong golden set danh dau `source_type = observed_or_adapted`.
- Quality bar chot: Dat khi >= 80% cau thu dat, va AI khong duoc bia thong tin khong co trong tai lieu du chi mot lan.
- Ket qua chay thu lan dau: 52/67, luu tai `eval/results_run_01.csv`. Day la baseline du doan/manual truoc khi chay batch tu dong qua API.

## §8. Phan cong & ke hoach

| Phan viec | Nguoi phu trach |
|---|---|
| Spec + quality bar | [TODO: ten + ma HV] |
| Evidence mining | [TODO: ten + ma HV] |
| Prompt + eval | [TODO: ten + ma HV] |
| Code prototype | [TODO: ten + ma HV] |
| Demo + validation | [TODO: ten + ma HV] |

- Willing users: [TODO: ten 1], [TODO: ten 2], [TODO: ten 3].
- Ke hoach validation CP5: moi user lam 1 task doc slide, 1 task hoi mo ho, 1 task hoi ngoai pham vi; ghi vao `validation/feedback_log.md`.
- Multi-prototype: khong lam trong phien ban nay; tap trung mot flow working.

## §9. Changelog

| Thoi diem | Doi gi | Vi sao |
|---|---|---|
| 2026-07-30 | Tao Streamlit prototype voi PDF viewer + tutor panel | Can show duoc thu bam duoc o CP2/CP3 |
| 2026-07-30 | Doi PDF viewer sang render PyMuPDF | Chrome chan iframe PDF local, can doc slide truc tiep trong app |
| 2026-07-30 | Chot quality bar 80% + zero hallucination | Bao ve loi nguoi hoc kho tu phat hien |
