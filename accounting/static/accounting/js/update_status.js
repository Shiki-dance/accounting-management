// CSRFトークンを取得する関数
function getCSRFToken() {
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    console.log(csrfInput ? csrfInput.value : 'CSRFトークンが見つかりません');
    return csrfInput ? csrfInput.value : '';
}

document.getElementById('payment-form').addEventListener('submit', function (event) {
    event.preventDefault(); // フォームのデフォルト送信を防ぐ

    const formData = new FormData(this); // フォームデータを取得
    const selectedStatuses = Array.from(formData.getAll('statuses')); // 選択されたIDを取得

    // サーバーにデータ送信
    fetch('/accounting/update_status_batch/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken(),
        },
        body: new URLSearchParams({
            statuses: selectedStatuses.join(','), 
        }),
    })
    
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('保存が成功しました！');
        } else {
            alert('保存に失敗しました。');
        }
    })
    .catch(error => {
        console.error('通信エラー:', error);
        alert('サーバーとの通信に失敗しました。');
    });
});


console.log('送信データ:', {
    status_id: statusId,
    is_paid: isPaid
});
