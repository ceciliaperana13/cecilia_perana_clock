class incromentation_temps:
      def start(self):
        # Démarrer un thread pour l'affichage et l'incrémentation du temps
        display_thread = threading.Thread(target=self._run_clock, daemon=True)
        display_thread.start()
        
        # Boucle principale pour les commandes utilisateur
        self._handle_commands()
      def _run_clock(self):
        """Thread qui gère l'affichage et l'incrémentation du temps"""
        while self.running:
            if not self.paused:
                self.display_time()
                self.check_alarm()
                time.sleep(1)
                self.increment_time()
    
      def _handle_commands(self):
        """Gère les commandes utilisateur en temps réel"""
        while self.running:
            try:
                command = input().strip().lower()
                self.paused = True
            except EOFError:
                  break    