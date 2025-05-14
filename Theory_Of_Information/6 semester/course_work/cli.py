import argparse
import os
import sys
from core.encoder import VideoEncoder
from core.decoder import VideoDecoder

def print_banner():
    """Вывод баннера приложения"""
    banner = """
╔══════════════════════════════════════════════════════════╗
║          Инструмент сжатия видео v1.0                   ║
║        Оптимизирован для высокой эффективности сжатия   ║
╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def validate_quality(value):
    """Проверка параметра качества (1-100)"""
    try:
        ivalue = int(value)
        if ivalue < 1 or ivalue > 100:
            raise argparse.ArgumentTypeError("Качество должно быть от 1 до 100")
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError("Качество должно быть числом")

def main():
    # Настройка парсера аргументов
    parser = argparse.ArgumentParser(
        description='Инструмент для эффективного сжатия видео',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''Примеры использования:
  Сжатие видео:  python cli.py encode -i input.mp4 -o output.vid -q 75
  Распаковка:    python cli.py decode -i output.vid -o output.mp4
  Подробный вывод: python cli.py encode -i input.mp4 -o output.vid -q 50 -v'''
    )
    
    # Общие аргументы
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    
    # Подпарсеры для разных команд
    subparsers = parser.add_subparsers(
        dest='command', 
        title='команды',
        description='Доступные команды',
        help='Выполняемая команда',
        metavar='{encode,decode}'
    )
    
    # Команда сжатия
    encode_parser = subparsers.add_parser(
        'encode', 
        help='Сжать видеофайл',
        description='Сжатие видеофайла с использованием DCT-сжатия',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    encode_parser.add_argument(
        '-i', '--input', 
        required=True, 
        help='Исходный видеофайл',
        metavar='ФАЙЛ'
    )
    encode_parser.add_argument(
        '-o', '--output', 
        required=True, 
        help='Выходной сжатый файл (рекомендуется .vid)',
        metavar='ФАЙЛ'
    )
    encode_parser.add_argument(
        '-q', '--quality', 
        type=validate_quality, 
        default=50, 
        help='Качество сжатия (1-100, больше - лучше качество)',
        metavar='1-100'
    )
    encode_parser.add_argument(
        '-k', '--keyframe-interval', 
        type=int, 
        default=10, 
        help='Интервал ключевых кадров (в кадрах)',
        metavar='N'
    )
    encode_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Подробный вывод с информацией о прогрессе'
    )
    
    # Команда распаковки
    decode_parser = subparsers.add_parser(
        'decode', 
        help='Распаковать видеофайл',
        description='Распаковка видеофайла в стандартный формат',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    decode_parser.add_argument(
        '-i', '--input', 
        required=True, 
        help='Сжатый файл (.vid)',
        metavar='ФАЙЛ'
    )
    decode_parser.add_argument(
        '-o', '--output', 
        required=True, 
        help='Выходной видеофайл',
        metavar='ФАЙЛ'
    )
    decode_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Подробный вывод с информацией о прогрессе'
    )
    
    # Разбор аргументов
    args = parser.parse_args()
    
    # Показать справку, если аргументы не указаны
    if len(sys.argv) == 1:
        print_banner()
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'encode':
            print_banner()
            print(f"[•] Сжатие:   {os.path.basename(args.input)}")
            print(f"[•] Выход:    {os.path.basename(args.output)}")
            print(f"[•] Качество: {args.quality}/100")
            print(f"[•] Ключ.кадр: Каждый {args.keyframe_interval} кадр")
            print("\n[ℹ] Начало сжатия...")
            
            encoder = VideoEncoder(
                output_file=args.output,
                quality=args.quality,
                keyframe_interval=args.keyframe_interval,
                verbose=args.verbose
            )
            encoder.encode(args.input)
            
            if not args.verbose:
                print("\n[✓] Сжатие успешно завершено!")
                
        elif args.command == 'decode':
            print_banner()
            print(f"[•] Распаковка: {os.path.basename(args.input)}")
            print(f"[•] Выход:     {os.path.basename(args.output)}")
            print("\n[ℹ] Начало распаковки...")
            
            decoder = VideoDecoder(
                input_file=args.input,
                verbose=args.verbose
            )
            decoder.decode(args.output)
            
            if not args.verbose:
                print("\n[✓] Распаковка успешно завершена!")
                
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"\n[✗] Ошибка: {str(e)}", file=sys.stderr)
        sys.exit(1)
    
    sys.exit(0)

if __name__ == '__main__':
    main()