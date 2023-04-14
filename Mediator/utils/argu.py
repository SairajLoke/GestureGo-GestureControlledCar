

def get_args():
    print('## Reading configuration ##')
    parser = configargparse.ArgParser(default_config_files=['config.txt'])

    parser.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
    parser.add("--device", type=int, default=0)
    parser.add("--width", help='cap width', type=int, default=960)
    parser.add("--height", help='cap height', type=int, default=540)

    parser.add("--is_keyboard", help='To use Keyboard control by default', type=bool, default=False)
    # parser.add('--use_static_image_mode', action='store_true', help='True if running on photos')
    parser.add("--min_detection_confidence",
               help='min_detection_confidence',
               type=float,
               default=0.7)
    parser.add("--min_tracking_confidence",
               help='min_tracking_confidence',
               type=float,
               default=0.7)
    parser.add("--buffer_len",
               help='Length of gesture buffer',
               type=int,
               default=10)

    args = parser.parse_args()

    return args