# Eval Coverage Summary

## 2. Tong so cau trong bo thu nghiem

67

## 3. Bo cau thu co bao nhieu kieu tinh huong?

4 kieu tinh huong, moi kieu co it nhat 2 cau:

| Kieu tinh huong | So case hien co | Vi du ID |
|---|---:|---|
| Thong tin can tra loi khong co trong tai lieu | 5 | HC_NOT_IN_DOC_01 |
| Cau mo ho, thieu ngu canh | 5 | HC_AMBIGUOUS_01 |
| Cau doi thu san pham khong duoc phep lam | 4 | HC_DISALLOWED_01 |
| Cau tra loi sai gay hau qua that | 5 | HC_HIGH_STAKES_01 |

## 4. So luong cau hoi bat nguon tu quan sat thuc te

11 case duoc danh dau `source_type = observed_or_adapted` trong `golden_set.json`.

Nguon gom chatlog VLearn trong `data/vlearn-pack/chatlog/`, mot case co lien quan OCR/context selection, va tinh huong nhom gap khi tu dung thu prototype.

## 5. Ket qua chay thu lan dau

52/67

Bang ket qua day du luu tai `eval/results_run_01.csv`.

## 6. Chuan dat cua nhom

Dat khi >= 80% cau thu dat, va AI khong duoc bia thong tin khong co trong tai lieu du chi mot lan.
