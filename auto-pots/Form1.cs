using System;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace auto_pots
{
    public partial class main_form : Form
    {
        private GlobalMouseHook _mouseHook;
        private CancellationTokenSource _cts;

        public main_form()
        {
            InitializeComponent();
            Load += Main_form_Load;
            FormClosing += Main_form_FormClosing;
        }

        private void Main_form_Load(object sender, EventArgs e)
        {
            _mouseHook = new GlobalMouseHook();
            _mouseHook.RightButtonDown += OnRightMouseDown;
            _mouseHook.RightButtonUp += OnRightMouseUp;
        }

        private void OnRightMouseDown()
        {
            if (_cts != null && !_cts.IsCancellationRequested)
                return;

            _cts = new CancellationTokenSource();
            var token = _cts.Token;

            Task.Run(async () =>
            {
                try
                {
                    while (!token.IsCancellationRequested)
                    {
                        // QWER scancodes for US layout
                        KeyboardSender.KeyPressScancode(0x10, 30); // Q
                        KeyboardSender.KeyPressScancode(0x11, 30); // W
                        KeyboardSender.KeyPressScancode(0x12, 30); // E
                        KeyboardSender.KeyPressScancode(0x13, 30); // R

                        await Task.Delay(100, token); // repeat delay
                    }
                }
                catch (TaskCanceledException)
                {
                }
            }, token);
        }

        private void OnRightMouseUp() => _cts?.Cancel();

        private void Main_form_FormClosing(object sender, FormClosingEventArgs e)
        {
            _cts?.Cancel();
            _mouseHook?.Dispose();
        }
    }
}
