document.querySelectorAll('.status-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', function () {
        const memberId = this.closest('tr').dataset.memberId;
        const status = this.checked;

        fetch('/update_status/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}',
            },
            body: JSON.stringify({
                member_id: memberId,
                status: status
            }),
        }).then(response => {
            if (!response.ok) {
                alert('更新に失敗しました。もう一度試してください。');
            }
        }).catch(() => {
            alert('サーバーとの通信に失敗しました。');
        });
    });
});
