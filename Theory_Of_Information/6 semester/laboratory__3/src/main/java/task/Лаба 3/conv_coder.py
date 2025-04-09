class ConvolutionalCoder:
    def __init__(self):
        self.polynomials = []
        self.verbose = False  # Флаг для вывода отладочной информации
        
    def set_polynomials(self, polynomials):
        """Установка полиномов для сверточного кодирования"""
        self.polynomials = polynomials
        
    def convolutional_encode(self, input_bits):
        """Сверточное кодирование"""
        if not self.polynomials:
            return None
            
        if not input_bits:
            return ''
        
        max_register = max(max(p) for p in self.polynomials)
        registers = [0] * (max_register + 1)
        encoded = []
        
        for bit in input_bits:
            registers.insert(0, int(bit))
            registers.pop()
            
            for poly in self.polynomials:
                xor = 0
                for idx in poly:
                    xor ^= registers[idx]
                encoded.append(str(xor))
        
        return ''.join(encoded)
    
    def viterbi_decode(self, encoded_bits):
        """Алгоритм Витерби для декодирования"""
        if not self.polynomials:
            return None
            
        if not encoded_bits:
            return ''
        
        n_outputs = len(self.polynomials)
        max_register = max(max(p) for p in self.polynomials)
        n_states = 2 ** max_register
        states = [format(i, f'0{max_register}b') for i in range(n_states)]
        
        if self.verbose:
            print("\n" + "═"*50)
            print(f"Начало декодирования. Параметры:")
            print(f"Количество состояний: {n_states}")
            print(f"Длина закодированной последовательности: {len(encoded_bits)} бит")
            print(f"Количество шагов: {len(encoded_bits)//n_outputs}")
        
        path_metrics = {s: float('inf') for s in states}
        path_metrics['0' * max_register] = 0
        paths = {s: [] for s in states}
    
        for step in range(0, len(encoded_bits)//n_outputs):
            current_bits = encoded_bits[step*n_outputs : (step+1)*n_outputs]
            new_metrics = {s: float('inf') for s in states}
            new_paths = {s: [] for s in states}
            
            if self.verbose:
                print("\n" + "─"*50)
                print(f"Шаг {step+1}. Полученные биты: {current_bits}")
            
            for state in states:
                if path_metrics[state] == float('inf'):
                    continue
                    
                if self.verbose:
                    print(f"\nСостояние: {state} (метрика: {path_metrics[state]:.1f})")
                
                for input_bit in ['0', '1']:
                    next_state = (input_bit + state)[:-1]
                    tmp_registers = list(map(int, input_bit + state))
                    
                    # Вычисляем ожидаемые выходные биты
                    expected = []
                    for poly in self.polynomials:
                        xor = sum(tmp_registers[idx] for idx in poly) % 2
                        expected.append(str(xor))
                    expected_str = ''.join(expected)
                    
                    # Вычисляем метрику Хэмминга
                    metric = sum(1 for a, b in zip(current_bits, expected_str) if a != b)
                    total_metric = path_metrics[state] + metric
                    
                    if self.verbose:
                        print(f"  Вход: {input_bit} -> Состояние: {next_state}")
                        print(f"  Ожидаемые: {expected_str} vs Фактические: {current_bits}")
                        print(f"  Метрика шага: {metric}, Общая метрика: {total_metric:.1f}")
                    
                    if total_metric < new_metrics[next_state]:
                        new_metrics[next_state] = total_metric
                        new_paths[next_state] = paths[state] + [input_bit]
                        if self.verbose:
                            print("  ✔ Обновление метрики")
                    elif self.verbose:
                        print("  ✖ Метрика хуже текущей")
    
            path_metrics, paths = new_metrics, new_paths
    
        if self.verbose:
            print("\n" + "═"*50)
            print("Финальные метрики состояний:")
            for state in sorted(path_metrics, key=lambda x: path_metrics[x]):
                print(f"{state}: {path_metrics[state]:.1f} → {paths[state]}")
    
        final_state = min(path_metrics, key=path_metrics.get)
        result = ''.join(paths[final_state])
        
        if self.verbose:
            print("\n" + "═"*50)
            print(f"Выбран путь: {paths[final_state]}")
            print(f"Финальная метрика: {path_metrics[final_state]:.1f}")
            print(f"Результат декодирования: {result}")
        
        return result[:len(encoded_bits)//len(self.polynomials)]

    def set_verbose(self, verbose):
        """Установка режима подробного вывода"""
        self.verbose = verbose 